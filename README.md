# humanoid-head-ros2
ROS2 + Gazebo humanoid emotional head simulation with expression state machine and PD control loop
# Humanoid Head ROS2

ROS2 + Gazebo humanoid emotional head simulation system.

A lightweight humanoid head simulation platform focused on:

- facial expression control
- state machine behavior
- PD closed-loop control
- robotics software architecture
- future Embodied AI / VLA integration

---

# Features

## Current Phase 1 Progress

- ROS2 package structure
- Gazebo simulation environment
- Humanoid head URDF model
- Eye / eyelid / jaw joints
- Expression state machine
- Automatic blinking
- PD control loop @50Hz
- ROS2 Topic command control
- 7 expression presets

---

# Tech Stack

- ROS2 Humble
- Gazebo Classic
- Python
- URDF
- ROS2 Topic Communication
- State Machine
- PD Controller

---

# Project Structure

```bash
humanoid_head_project/
├── urdf/
├── launch/
├── config/
├── worlds/
├── humanoid_head/
│   ├── expression_engine.py
│   ├── state_machine.py
│   ├── expression_defs.py
│   └── cli_handler.py
```

---

# Run

## Build

```bash
colcon build
source install/setup.bash
```

## Launch Gazebo Simulation

```bash
ros2 launch humanoid_head head_sim.launch.py
```

---

# Expression Commands

## Blink

```bash
ros2 topic pub /expression_command std_msgs/msg/String "data: 'blink'" -1
```

## Smile

```bash
ros2 topic pub /expression_command std_msgs/msg/String "data: 'smile'" -1
```

## Mouth Open

```bash
ros2 topic pub /expression_command std_msgs/msg/String "data: 'mouth_open'" -1
```

---

# Gazebo Simulation

## Current Status

- Model loading: DONE
- ROS2 communication: DONE
- Joint state publishing: DONE
- Expression state machine: DONE
- Physics joint movement: debugging

Currently debugging Gazebo joint physics behavior and preparing for:

- camera feedback loop
- TTS-driven jaw motion
- Isaac Sim migration
- future VLA integration

---

# Future Plan

- Vision feedback loop
- Voice synchronized facial motion
- Isaac Sim support
- Embodied AI integration
- VLM/VLA based interaction

---

# Screenshot

(Add Gazebo screenshots here)
