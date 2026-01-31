"""Constants for the NIBE DVC 10 integration."""
from typing import Final

DOMAIN: Final = "nibe_dvc10"

# UDP Communication
DEFAULT_PORT: Final = 4000
DEFAULT_TIMEOUT: Final = 2.0

# Protocol hex values
BASE_SEND_HEX: Final = "6d6f62696c65"  # "mobile"
BASE_RECV_HEX: Final = "6d6173746572"  # "master"

# Commands
CMD_GET_STATUS: Final = "010d"
CMD_TOGGLE_ONOFF: Final = "030d"
CMD_FAN_LOW: Final = "0401"
CMD_FAN_MEDIUM: Final = "0402"
CMD_FAN_HIGH: Final = "0403"
CMD_AIRFLOW_OUT: Final = "0600"      # One-way out [-->|-->]
CMD_AIRFLOW_RECOVERY: Final = "0601"  # Two-way recovery [<--|-->]
CMD_AIRFLOW_IN: Final = "0602"       # One-way in [-->|<--]
CMD_TOGGLE_DAYNIGHT: Final = "0901"

# Response data positions
POS_POWER: Final = 7       # 0=Off, 1=On
POS_MODE: Final = 9        # 0=Day, 1=Night, 2=Party
POS_FAN_SPEED: Final = 19  # 1=Low, 2=Medium, 3=High, 4=Manual
POS_MANUAL_SPEED: Final = 21  # 0x00-0xFF (9%-100%)
POS_AIRFLOW: Final = 23    # 0=Out, 1=Recovery, 2=In

# Fan speeds
FAN_SPEED_LOW: Final = 1
FAN_SPEED_MEDIUM: Final = 2
FAN_SPEED_HIGH: Final = 3
FAN_SPEED_MANUAL: Final = 4

FAN_SPEED_NAMES: Final = {
    FAN_SPEED_LOW: "low",
    FAN_SPEED_MEDIUM: "medium",
    FAN_SPEED_HIGH: "high",
    FAN_SPEED_MANUAL: "manual",
}

# Modes
MODE_DAY: Final = 0
MODE_NIGHT: Final = 1
MODE_PARTY: Final = 2

MODE_NAMES: Final = {
    MODE_DAY: "day",
    MODE_NIGHT: "night",
    MODE_PARTY: "party",
}

# Airflow modes
AIRFLOW_OUT: Final = 0
AIRFLOW_RECOVERY: Final = 1
AIRFLOW_IN: Final = 2

AIRFLOW_NAMES: Final = {
    AIRFLOW_OUT: "oneway_out",
    AIRFLOW_RECOVERY: "twoway",
    AIRFLOW_IN: "oneway_in",
}

AIRFLOW_DISPLAY_NAMES: Final = {
    AIRFLOW_OUT: "One-way Out [→→]",
    AIRFLOW_RECOVERY: "Two-way Recovery [←→]",
    AIRFLOW_IN: "One-way In [←←]",
}

# Polling interval
SCAN_INTERVAL: Final = 30  # seconds
