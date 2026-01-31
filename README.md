# NIBE DVC 10 Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/ergoliv/ha-nibe-dvc10.svg)](https://github.com/ergoliv/ha-nibe-dvc10/releases)
[![License](https://img.shields.io/github/license/ergoliv/ha-nibe-dvc10.svg)](LICENSE)

Home Assistant custom integration for **NIBE DVC 10** heat recovery ventilation units.

## Features

- 🔌 **On/Off control** - Turn the unit on or off
- 💨 **Fan speed control** - Low, Medium, High
- 🌙 **Mode selection** - Day, Night, Party modes
- 🔄 **Airflow direction** - One-way out, Two-way (recovery), One-way in
- 📊 **Status sensors** - Current state, temperature readings
- 🔧 **Multiple units support** - Control multiple DVC 10 units

## Supported Hardware

- NIBE DVC 10 (OEM version 2.0.1)
- OEM manufactured by VENTS
- Communication: UDP on port 4000

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu → "Custom repositories"
4. Add this repository URL: `https://github.com/ergoliv/ha-nibe-dvc10`
5. Select "Integration" as the category
6. Click "Add"
7. Search for "NIBE DVC 10" and install
8. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/nibe_dvc10` folder
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Via UI (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "NIBE DVC 10"
4. Enter the IP address of your unit
5. Optionally set a custom name

### Via YAML (Alternative)

```yaml
# configuration.yaml
nibe_dvc10:
  - host: 192.168.1.20
    name: "Living Room Ventilation"
  - host: 192.168.1.21
    name: "Bedroom Ventilation"
```

## Entities Created

For each configured unit, the following entities are created:

| Entity | Type | Description |
|--------|------|-------------|
| `fan.nibe_dvc10_<name>` | Fan | Main fan control with speed presets |
| `switch.nibe_dvc10_<name>` | Switch | On/Off control |
| `select.nibe_dvc10_<name>_mode` | Select | Day/Night/Party mode |
| `select.nibe_dvc10_<name>_airflow` | Select | Airflow direction |
| `sensor.nibe_dvc10_<name>_status` | Sensor | Current operational status |

## Services

### `nibe_dvc10.set_fan_speed`

Set the fan speed directly.

```yaml
service: nibe_dvc10.set_fan_speed
target:
  entity_id: fan.nibe_dvc10_living_room
data:
  speed: medium  # low, medium, high
```

### `nibe_dvc10.set_mode`

Set the operating mode.

```yaml
service: nibe_dvc10.set_mode
target:
  entity_id: fan.nibe_dvc10_living_room
data:
  mode: night  # day, night, party
```

### `nibe_dvc10.set_airflow`

Set the airflow direction.

```yaml
service: nibe_dvc10.set_airflow
target:
  entity_id: fan.nibe_dvc10_living_room
data:
  airflow: twoway  # oneway_out, twoway, oneway_in
```

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

The integration has a 1-second timeout. If your network is slow, the unit might not respond in time.

## Credits

- Protocol reverse engineering based on work by [@danielolsson100](https://github.com/danielolsson100/ha-nibedvc10)
- NIBE product info: [nibe.eu](https://www.nibe.eu/sv-se/produkter/ventilation/dvc-10)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
