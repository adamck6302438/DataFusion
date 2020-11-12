import math
import serial
import torch
import time
import datetime
import pprint

from random import randint
from sshtunnel import SSHTunnelForwarder
from model.SensorData import SensorData
from pymongo import MongoClient
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from algorithm.NN.NNv1 import get_KNNv1
from algorithm.NN.NNv4 import get_NNv4_ADC
from model.util.KalmanFilter import KalmanFilter
from typing import Tuple, List, Dict

from model.objects.points.Centroid import Centroid
from model.objects.points.GridPointADC import GridPointADC
from model.objects.points.Node import Node

node1 = Node("Node1", 1, 0, 1.5, 0)
node2 = Node("Node2", 2, 1.5, 1.5, 0)
node3 = Node("Node3", 3, 0, 0, 0)
node4 = Node("Node4", 4, 1.5, 0, 0)
node_list = [node1, node2, node3, node4]

grid_point_1 = GridPointADC("GP1", 1, {node1: 19, node2: 496, node3: 458, node4: 771}, 0.00, 1.50, 0.00)
grid_point_2 = GridPointADC("GP2", 2, {node1: 38, node2: 46, node3: 624, node4: 622}, 0.75, 1.50, 0.00)
grid_point_3 = GridPointADC("GP3", 3, {node1: 374, node2: 31, node3: 754, node4: 392}, 1.50, 1.50, 0.00)
grid_point_4 = GridPointADC("GP4", 4, {node1: 48, node2: 510, node3: 45, node4: 500}, 0.00, 0.75, 0.00)
grid_point_5 = GridPointADC("GP5", 5, {node1: 405, node2: 392, node3: 400, node4: 394}, 0.75, 0.75, 0.00)
grid_point_6 = GridPointADC("GP6", 6, {node1: 687, node2: 42, node3: 484, node4: 49}, 1.50, 0.75, 0.00)
grid_point_7 = GridPointADC("GP7", 7, {node1: 527, node2: 637, node3: 26, node4: 416}, 0.00, 0.00, 0.00)
grid_point_8 = GridPointADC("GP8", 8, {node1: 786, node2: 531, node3: 47, node4: 42}, 0.75, 0.00, 0.00)
grid_point_9 = GridPointADC("GP9", 9, {node1: 855, node2: 450, node3: 641, node4: 22}, 1.50, 0.00, 0.00)

# Centroid 1
grid_point_10 = GridPointADC("GP10", 10, {node1: 44, node2: 393, node3: 225, node4: 675}, 0.375, 1.125, 0.00)
# Centroid 2
grid_point_11 = GridPointADC("GP11", 11, {node1: 428, node2: 37, node3: 489, node4: 385}, 1.125, 1.125, 0.00)
# Centroid 3
grid_point_12 = GridPointADC("GP12", 12, {node1: 390, node2: 456, node3: 42, node4: 193}, 0.375, 0.375, 0.00)
# Centroid 4
grid_point_13 = GridPointADC("GP13", 13, {node1: 742, node2: 238, node3: 220, node4: 33}, 1.125, 0.375, 0.00)
grid_points = [grid_point_1, grid_point_2, grid_point_3, grid_point_4, grid_point_5, grid_point_6, grid_point_7,
               grid_point_8, grid_point_9, grid_point_10, grid_point_11, grid_point_12, grid_point_13]

centroid1 = Centroid(grid_point_10, grid_point_1, grid_point_2, grid_point_4, grid_point_5)
centroid2 = Centroid(grid_point_11, grid_point_2, grid_point_3, grid_point_5, grid_point_6)
centroid3 = Centroid(grid_point_12, grid_point_4, grid_point_5, grid_point_7, grid_point_8)
centroid4 = Centroid(grid_point_13, grid_point_5, grid_point_6, grid_point_8, grid_point_9)

centroids = [centroid1, centroid2, centroid3, centroid4]

# serial port config
ser = serial.Serial(
    port='/dev/cu.usbserial-1420', \
    baudrate=115200, \
)


def get_distance(default: int, adc: int) -> float:
    if default < 800:
        distance = (adc - 35.842) / 1.1115
    else:
        if adc < 680:
            distance = (adc + 165.14) / 10.989
        else:
            distance = (adc - 611.42) / 1.0385
    return distance


# NNv1
def calculate_NNv1(adcs: Dict[Node, int]) -> Tuple[float, float]:
    # calculate the received adc value from each node and compare to each grid point
    gp_list = grid_points
    for gp in gp_list:
        distances = 0
        for node, adc in adcs.items():
            distance = math.pow((get_distance(1000, adc) - get_distance(1000, gp.get_adcs(node))), 2)
            distances += distance
        try:
            distances = math.sqrt(distances)
            gp.distance = distances
        except RuntimeError:
            print("Error in distance calculation")

    for i in range(len(gp_list)):
        min_index = i
        for j in range(i + 1, len(gp_list)):
            if gp_list[min_index] > gp_list[j]:
                min_index = j

        gp_list[i], gp_list[min_index] = gp_list[min_index], gp_list[i]
    print(gp_list)
    x = round(((gp_list[0].x + gp_list[1].x + gp_list[2].x) / 3), 2)
    y = round(((gp_list[0].y + gp_list[1].y + gp_list[2].y) / 3), 2)
    return [x, y]


# NNv4
def calculate_NNv4(adcs: [Node, int] = None, list_adcs: Dict[Centroid, Dict[Node, int]] = None) -> Tuple[float, float]:
    centroid_points = centroids
    closest_centroid = centroids[0]
    smallest_distance = 0
    if adcs is not None and list_adcs is None:
        for cp in centroid_points:
            point = cp.Center
            distances = 0
            for node, adc in adcs.items():
                distance = math.pow((get_distance(1000, adc) - get_distance(1000, point.get_adcs(node))), 2)
                distances += distance
            distances = math.sqrt(distances)
            if cp == centroid_points[0]:
                smallest_distance = distances
            if distances < smallest_distance:
                smallest_distance = distances
                closest_centroid = cp
    if list_adcs is not None and adcs is None:
        for cp, adc in list_adcs.items():
            point = cp.Center
            distances = 0
            for node, adc in adcs.items():
                distance = math.pow((adc - point.get_rssis(node)), 2)
                distances += distance
            distances = math.sqrt(distances)
            if cp == centroid_points[0]:
                smallest_distance = distances
            if distances < smallest_distance:
                smallest_distance = distances
                closest_centroid = cp

    return closest_centroid.point


# read and store sensor values
def read_sensor_data() -> Dict[Node, int]:
    sensor_values = [0, 0, 0, 0]
    while True:
        try:
            test = ser.readline()
            string_t = test.decode()
            string = string_t.rstrip()
            string = string.replace("Node: ", "")
            string = string.replace(",ADC: ", "")
            input = string.split()
            sensor_num = int(input[0])
            sensor_val = int(input[1])
            print(sensor_num)
            print(sensor_val)
            if sensor_num == 1:
                sensor_values[0] = sensor_val
            elif sensor_num == 2:
                sensor_values[1] = sensor_val
            elif sensor_num == 3:
                sensor_values[2] = sensor_val
            elif sensor_num == 4:
                sensor_values[3] = sensor_val
        except:
            continue
        if sensor_values[0] != 0 and sensor_values[1] != 0 and sensor_values[2] != 0 and sensor_values[3] != 0:
            break

    return {node1: sensor_values[0], node2: sensor_values[1], node3: sensor_values[2], node4: sensor_values[3]}


def check_for_fire():

    return 0

def send_location():


if __name__ == '__main__':
    while True:
        read_adc = read_sensor_data()
        print(read_adc)
        coordinate = calculate_NNv4(adcs=read_adc)
        print(coordinate)

