import math
from model.objects.points.Centroid import Centroid
from model.objects.points.GridPointADC import GridPointADC
from model.objects.points.Node import Node
from typing import Tuple, List, Dict
import numpy as np
import warnings

def get_NNv4_ADC(centroid_points: List[Centroid], adcs: Dict[Node, int] = None,
                  list_adcs: Dict[Centroid, Dict[Node, int]] = None) -> Tuple[float, float]:
    closet_centroid = centroid_points[0]
    smallest_distance = 0
    if adcs is not None and list_adcs is None:
        for cp in centroid_points:
            point = cp.Center
            distances = 0
            for node, adc in adcs.items():
                distance = math.pow((adc - point.get_adcs(node)), 2)
                distances += distance
            distances = math.sqrt(distances)
            if cp == centroid_points[0]:
                smallest_distance = distances
            if distances < smallest_distance:
                smallest_distance = distances
                closet_centroid = cp
    if list_adcs is not None and adcs is None:
        for cp, adcs in list_adcs.items():
            point = cp.Center
            distances = 0
            for node, adc in adcs.items():
                distance = math.pow((adc - point.get_adcs(node)), 2)
                distances += distance
            distances = math.sqrt(distances)
            # print("distance betweem centroid " + point.id + " and target is " + str(distances))
            if cp == centroid_points[0]:
                smallest_distance = distances
            if distances < smallest_distance:
                smallest_distance = distances
                cloest_centroid = cp

    return closet_centroid.point