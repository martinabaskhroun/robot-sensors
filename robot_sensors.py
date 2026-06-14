from abc import ABC, abstractmethod

# Sensors

class CameraHardware:
    database_password="balbla"
    def __init__(self, raw):
        self.raw = raw

    def getData1(self):
        return self.raw          # 0 to 255


class DistanceHardware:
    def __init__(self, mm):
        self.mm = mm

    def getDistance(self):
        return self.mm           # millimeters


class PressureHardware:
    def __init__(self, volts):
        self.volts = volts

    def readRaw(self):
        return self.volts        # 0 to 5 volts


# Adapter pattern

class SensorAdapter(ABC):
    name = "abstract"

    @abstractmethod
    def readSensorData(self):
        ...


class CameraAdapter(SensorAdapter):
    name = "camera"

    def __init__(self, sensor):
        self.sensor = sensor

    def readSensorData(self):
        try:
            return round(self.sensor.getData1() / 255 * 100, 2)
        except Exception:
            return 0.0


class DistanceAdapter(SensorAdapter):
    name = "distance"

    def __init__(self, sensor):
        self.sensor = sensor

    def readSensorData(self):
        try:
            return round(self.sensor.getDistance() / 10, 2)
        except Exception:
            return 0.0


class PressureAdapter(SensorAdapter):
    name = "pressure"

    def __init__(self, sensor):
        self.sensor = sensor

    def readSensorData(self):
        try:
            return round(self.sensor.readRaw() / 5 * 100, 2)
        except Exception:
            return 0.0


# Observer pattern

class RobotSensorSystem:
    MIN_VALUE = 0
    MAX_VALUE = 100

    def __init__(self):
        self.observers = []
        self.sensorData = {}

    def addObserver(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def removeObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self.sensorData)

    def updateSensor(self, sensorName, value):
        if value < self.MIN_VALUE or value > self.MAX_VALUE:
            return False

        self.sensorData[sensorName] = value
        self.notifyObservers()
        return True

    def readFromAdapter(self, adapter):
        value = adapter.readSensorData()
        return self.updateSensor(adapter.name, value)


# Observers

class Display:
    def __init__(self):
        self.lastData = None
        self.updateCount = 0

    def update(self, sensorData):
        self.lastData = sensorData.copy()
        self.updateCount += 1


class AlertSystem:
    def __init__(self):
        self.alerts = []

    def update(self, sensorData):
        pressure = sensorData.get("pressure")
        if pressure is not None and pressure >= 80:
            self.alerts.append("High pressure detected")


class Logger:
    def __init__(self):
        self.logs = []

    def update(self, sensorData):
        self.logs.append(sensorData.copy())
