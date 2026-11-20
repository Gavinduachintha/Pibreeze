# 🌬️ PiBreeze

<p align="center">
  <strong>Stay cool. Stay in control.</strong>
  <br/>
  A lightweight desktop application for Raspberry Pi 5 fan control and real-time system monitoring.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%205-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white" alt="Raspberry Pi 5"/>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GUI-Tkinter-4FDA8E?style=for-the-badge&logo=windowsterminal&logoColor=black" alt="Tkinter"/>
  <img src="https://img.shields.io/badge/OS-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
</p>

---

## Overview

**PiBreeze** is a Python-based desktop utility developed to simplify cooling management on the Raspberry Pi 5.

It provides a graphical interface for controlling fan speed and monitoring essential system metrics without constantly relying on terminal commands.

Built with Python and Tkinter, PiBreeze interacts with Linux hardware interfaces to provide fan PWM control, CPU temperature monitoring, and processor clock-speed information.

Whether you want to manually adjust cooling performance or monitor your Raspberry Pi's thermal behavior, PiBreeze brings these controls together in one simple interface.

## Interface Preview

<p align="center">
  <img src="assets/pi-breeze-preview.png" alt="PiBreeze application interface" width="700"/>
  <br/>
  <sub>PiBreeze – Raspberry Pi 5 Cooling Management</sub>
  <img width="722" height="957" alt="image" src="https://github.com/user-attachments/assets/9982c2a8-205a-427e-be25-90f54f8c0c33" />

</p>


## Features

| Feature | Description |
|---|---|
| 🌬️ Fan Speed Control | Adjust fan speed using an interactive slider |
| ⚡ Fan Status | View the current fan operating state |
| 🌡️ CPU Temperature | Monitor processor temperature |
| 🕒 CPU Clock Speed | Track the current processor frequency |
| 🎛️ PWM Management | Control fan output through Linux hardware interfaces |
| 🔄 Automatic Mode | Restore automatic fan control when supported |
| 📊 System Monitoring | Display essential hardware metrics through the GUI |

## Tech Stack

<p>
  <img src="https://skillicons.dev/icons?i=python,linux,raspberrypi" alt="Technology stack"/>
</p>

- **Python 3** – Application logic and system interaction.
- **Tkinter** – Desktop graphical user interface.
- **Linux sysfs** – Hardware monitoring and PWM control.
- **Raspberry Pi 5** – Target hardware platform.

## Hardware Requirements

- Raspberry Pi 5
- Compatible PWM-controlled cooling fan
- Raspberry Pi OS or compatible Linux distribution
- Python 3
- Tkinter

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gavinduachintha/PiBreeze.git
cd PiBreeze
```

### 2. Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-tk
```

PiBreeze uses Python's standard library and Tkinter, so additional Python packages may not be necessary.

### 3. Run the application

```bash
python3 main.py
```

Depending on your system configuration, elevated permissions may be required for fan control operations.

## How It Works

PiBreeze communicates with Raspberry Pi hardware interfaces exposed through the Linux kernel.

It uses the following interfaces:

| Interface | Purpose |
|---|---|
| `/sys/class/hwmon/` | Access hardware monitoring information |
| `pwm1` | Configure fan PWM output |
| `pwm1_enable` | Manage PWM operating mode |
| `/sys/class/thermal/` | Retrieve CPU temperature |
| `/sys/devices/system/cpu/` | Retrieve CPU frequency information |

The application reads system metrics and updates the graphical interface while allowing the user to modify fan control settings.

*Note: Hardware interface paths and available PWM controls may vary depending on the Linux kernel, device configuration, and active hardware driver.*

## Project Structure

```text
PiBreeze/
│
├── main.py
│
├── assets/
│   └── pi-breeze-preview.png
│
└── README.md
```

## Safety Notes

- Designed primarily for Raspberry Pi 5.
- Use a compatible cooling fan and PWM interface.
- Fan control may require elevated permissions.
- Monitor CPU temperature when experimenting with manual fan speeds.
- Ensure automatic thermal management is restored when appropriate.
- Avoid disabling cooling while the processor is under heavy workloads.

## Future Improvements

- [ ] Configurable temperature-based fan curves.
- [ ] Custom fan speed profiles.
- [ ] Temperature history and monitoring graphs.
- [ ] Automatic startup integration.
- [ ] Additional hardware monitoring metrics.

## License

This project is open-source. A license will be added to the repository to define its distribution and reuse permissions.

---

<p align="center">
  <strong>🌬️ PiBreeze</strong>
  <br/>
  <sub>Stay cool. Stay in control.</sub>
  <br/><br/>
  Developed by <a href="https://github.com/Gavinduachintha">Gavindu Achintha</a>
  <br/>
  <a href="https://github.com/Gavinduachintha/PiBreeze">GitHub Repository</a>
</p>
