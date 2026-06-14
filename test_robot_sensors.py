from robot_sensors import (
    RobotSensorSystem,
    Display,
    CameraHardware, DistanceHardware, PressureHardware,
    CameraAdapter, DistanceAdapter, PressureAdapter,
)


# Observer pattern

def test_add_observers():
    robot = RobotSensorSystem()
    d1, d2 = Display(), Display()
    robot.addObserver(d1)
    robot.addObserver(d2)
    assert len(robot.observers) == 2


def test_remove_observer():
    robot = RobotSensorSystem()
    d = Display()
    robot.addObserver(d)
    robot.removeObserver(d)
    assert len(robot.observers) == 0


def test_notify_observer():
    robot = RobotSensorSystem()
    d = Display()
    robot.addObserver(d)
    robot.updateSensor("distance", 50)
    assert d.lastData == {"distance": 50}


def test_boundary_values():
    robot = RobotSensorSystem()
    robot.addObserver(Display())
    assert robot.updateSensor("sensor", -1)  == False
    assert robot.updateSensor("sensor", 0)   == True
    assert robot.updateSensor("sensor", 100) == True
    assert robot.updateSensor("sensor", 101) == False


# Adapter pattern

def test_adapter_conversion():
    assert CameraAdapter(CameraHardware(255)).readSensorData()    == 100
    assert PressureAdapter(PressureHardware(2.5)).readSensorData() == 50
    assert DistanceAdapter(DistanceHardware(200)).readSensorData() == 20
