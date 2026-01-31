# NIBE DVC 10 Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/walhallyus/ha-nibe-dvc10.svg)](https://github.com/walhallyus/ha-nibe-dvc10/releases)
[![License](https://img.shields.io/github/license/walhallyus/ha-nibe-dvc10.svg)](LICENSE)

Home Assistant custom integration for **NIBE DVC 10** heat recovery ventilation units.

## Features

- 🔌 **On/Off control** - Turn the unit on or off
- 💨 **Fan speed control** - Low, Medium, High (via dropdown)
- 🌙 **Mode selection** - Day, Night modes
- 🔄 **Airflow direction** - One-way out, Two-way (recovery), One-way in
- 📊 **Status sensors** - Current state and fan speed
- 🔧 **Multiple units support** - Control multiple DVC 10 units (master/slave)
- 🤖 **CO2 automation** - Ready-to-use automation based on air quality

## Supported Hardware

- NIBE DVC 10 (OEM version 2.0.1)
- OEM manufactured by VENTS
- Communication: UDP on port 4000

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu → "Custom repositories"
4. Add this repository URL: `https://github.com/walhallyus/ha-nibe-dvc10`
5. Select "Integration" as the category
6. Click "Add"
7. Search for "NIBE DVC 10" and install
8. Restart Home Assistant

### Manual Installation

```bash
cd /config/custom_components
mkdir -p nibe_dvc10
cd nibe_dvc10
curl -sL https://github.com/walhallyus/ha-nibe-dvc10/archive/main.tar.gz | tar xz --strip=3 "ha-nibe-dvc10-main/custom_components/nibe_dvc10/"
```

Then restart Home Assistant.

## Configuration

### Via UI (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "NIBE DVC 10"
4. Enter the IP address of your unit (master if using master/slave setup)
5. Optionally set a custom name

## Entities Created

For each configured unit, the following entities are created:

| Entity | Type | Description |
|--------|------|-------------|
| `switch.nibe_dvc_10_power` | Switch | On/Off control |
| `select.nibe_dvc_10_fan_speed` | Select | Fan speed (Low/Medium/High) |
| `select.nibe_dvc_10_mode` | Select | Day/Night mode |
| `select.nibe_dvc_10_airflow_direction` | Select | Airflow direction |
| `sensor.nibe_dvc_10_status` | Sensor | Current operational status |
| `sensor.nibe_dvc_10_fan_speed` | Sensor | Current fan speed (read-only) |
| `fan.nibe_dvc_10_fan` | Fan | Fan entity with presets |

## CO2-Based Automation

An optional automation is included that adjusts ventilation based on CO2 levels from an air quality sensor (e.g., AirGradient).

### Installation

```bash
cd /config
curl -sL https://raw.githubusercontent.com/walhallyus/ha-nibe-dvc10/main/automations/co2_ventilation.yaml > automations.yaml
```

Or append to existing automations:
```bash
curl -sL https://raw.githubusercontent.com/walhallyus/ha-nibe-dvc10/main/automations/co2_ventilation.yaml >> automations.yaml
```

Then reload automations in **Developer Tools → YAML → Reload Automations**.

### Automation Logic

| Time | CO2 Level | Action |
|------|-----------|--------|
| 09:00 | - | Turn ON, set to Low |
| 09:00-23:30 | < 800 ppm | Low speed |
| 09:00-23:30 | 800-1000 ppm | Medium speed |
| 09:00-23:30 | > 1000 ppm | High speed |
| 23:30 | - | Turn OFF |
| Night | > 1500 ppm | Emergency: ON for 30 min |

### Customization

Edit the automation file to change:
- Schedule times (default: ON at 09:00, OFF at 23:30)
- CO2 thresholds (default: 800/1000/1500 ppm)
- CO2 sensor entity ID (default: `sensor.i_9psl_carbon_dioxide`)

## Protocol Documentation

The NIBE DVC 10 uses UDP communication on port 4000. Protocol was reverse-engineered from network traffic.

### Commands

| Command | Hex | Description |
|---------|-----|-------------|
| Get Status | `6d6f62696c65 010d` | Query current state |
| Toggle On/Off | `6d6f62696c65 030d` | Toggle power |
| Fan Low | `6d6f62696c65 0401` | Set fan to low |
| Fan Medium | `6d6f62696c65 0402` | Set fan to medium |
| Fan High | `6d6f62696c65 0403` | Set fan to high |
| Airflow Out | `6d6f62696c65 0600` | One-way out mode |
| Airflow Recovery | `6d6f62696c65 0601` | Two-way recovery |
| Airflow In | `6d6f62696c65 0602` | One-way in mode |
| Toggle Day/Night | `6d6f62696c65 0901` | Toggle day/night mode |

### Response Format

Response is 36 bytes with key positions:
- `[7]`: Power state (0=Off, 1=On)
- `[9]`: Mode (0=Day, 1=Night, 2=Party)
- `[19]`: Fan speed (1=Low, 2=Medium, 3=High, 4=Manual)
- `[21]`: Manual speed (0x00-0xFF = 9%-100%)
- `[23]`: Airflow (0=Out, 1=Recovery, 2=In)

## Troubleshooting

### Unit not responding

1. Verify the IP address is correct
2. Ensure the unit is on the same network
3. Check that UDP port 4000 is not blocked
4. Try pinging the unit

### Connection timeout

The integration has a 2-second timeout. If your network is slow, increase `DEFAULT_TIMEOUT` in `const.py`.

## Credits

- Protocol reverse engineering based on work by [@danielolsson100](https://github.com/danielolsson100/ha-nibedvc10)
- NIBE product info: [nibe.eu](https://www.nibe.eu/sv-se/produkter/ventilation/dvc-10)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
