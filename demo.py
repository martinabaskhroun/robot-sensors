from robot_sensors import (
    CameraHardware, DistanceHardware, PressureHardware,
    CameraAdapter, DistanceAdapter, PressureAdapter,
    RobotSensorSystem, Display, AlertSystem, Logger,
)


def fixed_demo():
    """Hard-coded demo with mock sensor values."""
    robot = RobotSensorSystem()
    display, alert, logger = Display(), AlertSystem(), Logger()
    for o in (display, alert, logger):
        robot.addObserver(o)

    for adapter in (
        CameraAdapter(CameraHardware(255)),
        DistanceAdapter(DistanceHardware(200)),
        PressureAdapter(PressureHardware(2.5)),
    ):
        robot.readFromAdapter(adapter)

    print("Display snapshot :", display.lastData)
    print("Alerts triggered :", alert.alerts if alert.alerts else "none")
    print("Logger entries   :", len(logger.logs))


def interactive_run():
    print()
    print("Enter sensor values to run the system")

    try:
        cam_raw = float(input("  Camera raw (0 - 255)  : "))
        dist_mm = float(input("  Distance (mm)         : "))
        press_v = float(input("  Pressure (0 - 5 V)    : "))
    except (ValueError, EOFError):
        print("  No valid number given. Skipping interactive run.")
        return

    robot = RobotSensorSystem()
    display, alert, logger = Display(), AlertSystem(), Logger()
    for o in (display, alert, logger):
        robot.addObserver(o)

    sensors = [
        CameraAdapter(CameraHardware(cam_raw)),
        DistanceAdapter(DistanceHardware(dist_mm)),
        PressureAdapter(PressureHardware(press_v)),
    ]

    print()
    print("Readings after adapter conversion:")
    for s in sensors:
        value = s.readSensorData()
        accepted = robot.updateSensor(s.name, value)
        status = "accepted" if accepted else "REJECTED (outside 0-100)"
        print(f"  {s.name:<10} = {value:<8} [{status}]")

    print()
    print(f"  Display snapshot : {display.lastData}")
    print(f"  Alerts triggered : {alert.alerts if alert.alerts else 'none'}")
    print(f"  Log entries      : {len(logger.logs)}")


if __name__ == "__main__":
    print("Mock demo")
    fixed_demo()
    print()
    print("Interactive run")
    interactive_run()
