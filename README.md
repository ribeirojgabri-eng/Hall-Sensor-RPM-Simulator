# Concept S - Hall Sensor RPM Simulator

## Overview

This project is a Python-based simulation of a Hall effect sensor system for rotational RPM acquisition.

The main objective is to study rotational pulse detection, temporal consistency, and RPM measurement logic using a virtual rotating shaft and real-time signal processing concepts.

The simulation was developed as an early-stage prototype for the "Concept S" project.

---

## Main Features

* Real-time rotational simulation
* Hall sensor pulse detection
* RPM acquisition logic
* Delta time based simulation
* Temporal consistency independent from FPS
* Rotational pulse counting
* Real-time RPM measurement
* Visual telemetry interface
* High RPM pulse-loss correction

---

## Technologies Used

* Python
* Pygame

---

## Mathematical Concepts

### Angular Velocity Conversion

RPM values are converted into angular velocity:

ω = RPM × 360 / 60

Where:

* RPM = rotations per minute
* 360 = degrees per rotation
* 60 = seconds per minute

---

### Angular Position Update

The angular position is updated using delta time integration:

θ = θ + ωΔt

Where:

* θ = angular position
* ω = angular velocity
* Δt = elapsed time between frames

This prevents the simulation from depending on frame rate (FPS).

---

## Problem Identified in the First Version

The initial implementation used a frame-dependent rotational update.

This caused:

* inconsistent simulation speed
* incorrect angular behavior
* pulse loss at high RPM values

At high rotational speeds, multiple rotations could occur between two rendered frames, causing missed pulse detections.

---

## Implemented Solution

The current version uses accumulated angular displacement and integer rotation tracking.

The system calculates:

N = floor(θ / 360)

This allows correct pulse counting even when multiple rotations occur between frames.

---

## Current Status

Current implemented systems:

* rotational simulation
* Hall sensor visualization
* RPM acquisition
* pulse counting
* temporal correction
* measurement validation

Next planned steps:

* Arduino implementation
* Tinkercad simulation
* hardware pulse acquisition
* interrupt-based reading
* digital dashboard integration

---

## Objective of the Project

The purpose of this project is educational and experimental.

The project is being used to study:

* embedded systems concepts
* rotational sensing
* telemetry logic
* real-time simulation
* signal acquisition
* mathematical modeling

---

## Author

Developed by João Gabriel as part of the Concept S project.
