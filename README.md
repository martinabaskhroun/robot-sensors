## Why Python

Small exercise, so a scripting language with no compile step keeps the focus on design.

`abc` gives a real abstract base class with no external dependency.

## Files

README.md               <- this file (setup, tests, patterns, deviations)
robot_sensors.py        <- Patterns (Adapter + Observer)
demo.py                 <- mock data + interactive run
test_robot_sensors.py   <- pytest test suite


## How to run

Open a terminal in the project folder.

### Setup

```bash
pip install pytest
```

### Demo

```bash
python demo.py
```

### Tests

```bash
pytest -v
```


## What's tested


test_add_observers: Add observers
test_remove_observer: Remove an observer 
test_notify_observer:  Notification reaches observer with right data
test_boundary_values: EP/BVA gate rejects -1 and 101, accepts 0 and 100 
test_adapter_conversion: Each adapter converts its hardware reading 

Expected:

```
test_robot_sensors.py::test_add_observers PASSED
test_robot_sensors.py::test_remove_observer PASSED
test_robot_sensors.py::test_notify_observer PASSED
test_robot_sensors.py::test_boundary_values PASSED
test_robot_sensors.py::test_adapter_conversion PASSED

5 passed
```


### Adapter pattern

For the Adapter, I split the team's single SensorAdapter into three small classes
(CameraAdapter, DistanceAdapter, PressureAdapter) that share an abstract base.
Adding a new sensor later means writing one new class instead of editing an existing one.

Each adapter handles its own unit conversion (255 -> 100 %, mm -> cm, V -> 0-100 %)
and falls back to 0.0 if the hardware fails.

Sensor1 / 2 / 3 were renamed to CameraHardware / DistanceHardware / PressureHardware
for readability.

### Observer pattern

For the Observer, the names match the pseudo (addObserver, removeObserver, notifyObservers,
updateSensor, sensorData).

I added a validation gate in updateSensor that rejects values outside 0-100, which is the
EP/BVA table is checking.

Small `in / not in` guards on add and remove keep them safe against duplicates or missing observers.
A readFromAdapter helper connects the two patterns: read from the adapter, push through the gate.

The pseudo's three observers all just printed; I replaced them with Display, AlertSystem,
and Logger so each one has its own job.

### Test concept

for the tests, the runner prints PASS or FAIL per test and exits non-zero on any failure.

Before the tests, an interactive prompt lets the marker enter sensor values and watch the validation
gate accept or reject them; a non-number or empty input skips it.

Test count and EP/BVA scope. The team plan lists five Observer scenarios and a nine-row EP/BVA table.
The five scenarios are all present as Python functions. The boundary test covers four of the nine rows 
(-1, 0, 100, 101); the partition cases (-10, 50, 120) and just-inside cases (1, 99) are still on the 
to-do list.