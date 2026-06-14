# Robot Sensor System
 
A Python implementation of the **Adapter** and **Observer** design patterns applied to a multi-sensor robotic system. Built as a clean, extensible architecture for reading, normalising, and reacting to data from heterogeneous hardware sensors.
 
---
 
## Overview
 
Real robots talk to many different sensors, each with its own data format and units. This project solves two classic problems:
 
- **Adapter pattern** — wraps incompatible sensor hardware behind a unified interface, handling unit conversion per sensor type
- **Observer pattern** — decouples the sensor system from downstream consumers (display, alerts, logging) so each reacts independently to new readings
---
 
## Architecture
 
```
Hardware
  CameraHardware    (raw 0–255)      →  CameraAdapter    (raw / 255 × 100)
  DistanceHardware  (millimetres)    →  DistanceAdapter  (mm / 10)
  PressureHardware  (0–5 V)         →  PressureAdapter  (V / 5 × 100)
 
                          ↓ readSensorData() → 0–100
 
                    RobotSensorSystem
                      validate: reject if < 0 or > 100
                      store: sensorData[name] = value
                      notify: all observers
 
                          ↓ update(sensorData)
 
  Display           stores latest snapshot + update count
  AlertSystem       appends alert if pressure ≥ 80
  Logger            appends snapshot to history
```
 
### Adapter layer
Each adapter converts raw hardware output to a normalised 0–100 scale:
 
| Adapter           | Hardware output | Conversion         |
|-------------------|-----------------|--------------------|
| `CameraAdapter`   | 0–255 raw       | `raw / 255 × 100`  |
| `DistanceAdapter` | millimetres     | `mm / 10`          |
| `PressureAdapter` | 0–5 volts       | `V / 5 × 100`      |
 
Adding a new sensor = writing one new class. No existing code changes.
 
### Observer layer
`RobotSensorSystem` maintains a list of observers and notifies all of them on every valid sensor update. A validation gate rejects values outside the 0–100 range before any notification fires.
 
| Observer      | Behaviour                                      |
|---------------|------------------------------------------------|
| `Display`     | Stores the latest snapshot and update count    |
| `AlertSystem` | Appends an alert when pressure ≥ 80            |
| `Logger`      | Keeps a full history of every sensor state     |
 
---
 
## Files
 
| File                    | Purpose                              |
|-------------------------|--------------------------------------|
| `robot_sensors.py`      | Core implementation (Adapter + Observer) |
| `demo.py`               | Mock data demo + interactive CLI run |
| `test_robot_sensors.py` | pytest test suite                    |
 
---
 
## Getting Started
 
### Requirements
 
```bash
pip install pytest
```
 
### Run the demo
 
```bash
python demo.py
```
 
The demo runs a fixed mock scenario first, then prompts you to enter your own sensor values to watch the validation gate accept or reject them live.
 
### Run the tests
 
```bash
pytest -v
```
 
Expected output:
 
```
test_robot_sensors.py::test_add_observers       PASSED
test_robot_sensors.py::test_remove_observer     PASSED
test_robot_sensors.py::test_notify_observer     PASSED
test_robot_sensors.py::test_boundary_values     PASSED
test_robot_sensors.py::test_adapter_conversion  PASSED
 
5 passed
```
 
---
 
## Test Coverage
 
| Test                    | What it checks                                         |
|-------------------------|--------------------------------------------------------|
| `test_add_observers`    | Multiple observers register correctly                  |
| `test_remove_observer`  | Observer removal works without side effects            |
| `test_notify_observer`  | Notification delivers correct data to observer         |
| `test_boundary_values`  | Gate rejects −1 and 101, accepts 0 and 100 (EP/BVA)   |
| `test_adapter_conversion` | Each adapter converts its hardware reading accurately |
 
---
 
## Design Decisions
 
- **One adapter per sensor type** rather than a single monolithic adapter — satisfies the Open/Closed Principle; new sensors require only a new class
- **Validation gate in `updateSensor`** — keeps invalid readings out of the observer pipeline entirely
- **Named hardware classes** (`CameraHardware`, `DistanceHardware`, `PressureHardware`) instead of generic `Sensor1/2/3` for readability
- **Distinct observer roles** (`Display`, `AlertSystem`, `Logger`) instead of three identical print observers — each has a single, testable responsibility
