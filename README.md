# Screen Monitor

A Python-based system monitoring tool designed for dual OLED displays (SH1106 and SH1107) connected via I2C.

## Features

- **Dual Display Support**:
    - **SH1106** (128x64) for battery and power status.
    - **SH1107** (128x128) for network traffic (upload/download speeds).
- **Real-time Monitoring**: Tracks battery percentage, power consumption (Watts), and network throughput.
- **Adaptive Brightness**: Automatically adjusts contrast for "night mode" between 22:00 and 07:00.
- **Dynamic Scaling**: Network speeds automatically scale between Kbps and Mbps.

## Hardware Requirements

- 1x SH1106 OLED Display (Default: I2C Port 4, Address `0x3C`)
- 1x SH1107 OLED Display (Default: I2C Port 5, Address `0x3C`)
- A Linux-based system with I2C enabled (e.g., Raspberry Pi, Orange Pi).

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

```bash
# Install dependencies
uv sync
```

## Usage

Start the monitor:

```bash
uv run screen.py
```

To test the displays with a static image or solid color:

```bash
uv run image_test.py
```

## Data Input

The script expects a `data.json` file in the root directory to provide battery and power metrics. This is typically updated by a background process or service.

```json
{
    "ups_percent": 85.0,
    "watt": 5.2,
    "power_state": "Discharging"
}
```
