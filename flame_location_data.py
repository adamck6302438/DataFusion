import serial
import time
import datetime
from pymongo import MongoClient
from random import randint
from sshtunnel import SSHTunnelForwarder
import pprint

# mongodb connection
MONGO_HOST = "192.168.0.243"
MONGO_DB = "business"
MONGO_USER = "ray"
MONGO_PASS = "2324"
server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)

server.start()
client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client.sensorData
col = client.db.flameLocation

# serial port
ser = serial.Serial('/dev/cu.usbserial-1420')
time.sleep(10)

data_list = []