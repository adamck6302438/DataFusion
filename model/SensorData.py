class SensorData:
    temperature = 0.0
    def __init__(self, temperature, humidity, infrared, gas, co):
        self.temperature = temperature
        self.humidity = humidity
        self.infrared = infrared
        self.gas = gas
        self.co = co

    def __str__(self):
        return "Temperature: " + str(self.temperature) + " C ,Humidity: " + str(self.humidity) + "% ,Infrared: " + str(self.infrared) + ", Gas: " + str(self.gas) + ", CO: "+ str(self.co)