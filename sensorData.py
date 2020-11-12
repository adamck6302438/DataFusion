import serial
import time
import datetime
from pymongo import MongoClient
from random import randint
from sshtunnel import SSHTunnelForwarder
import pprint
from model.SensorData import SensorData

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
col = client.db.test


# serial port
ser = serial.Serial('/dev/cu.usbserial-1420')
time.sleep(10)

data_list = []

# read serial port and write to mongodb
for i in range(2):
    temperature=ser.readline()
    string_t = temperature.decode()
    string = string_t.rstrip()
    temp = float(string)

    humidity=ser.readline()
    string_t = humidity.decode()
    string = string_t.rstrip()
    hum = float(string)

    infrared=ser.readline()
    string_t = infrared.decode()
    string = string_t.rstrip()
    infr = float(string)

    gas=ser.readline()
    string_t = temperature.decode()
    string = string_t.rstrip()
    g = float(string)

    co=ser.readline()
    string_t = co.decode()
    string = string_t.rstrip()
    c = float(string)

    dataPoint = {
        "temperature": temp,
        "infrared": infr,
        "gas": g,
        "co": c,
        "humidity": hum,
        "timestamp": datetime.datetime.now()
    }

    result = col.insert_one(dataPoint)

    # dataPoint = SensorData(temperature=temp, humidity=hum, infrared=infr, gas=g, co=c)
    # data_list.append(dataPoint)

# stop server
server.stop()