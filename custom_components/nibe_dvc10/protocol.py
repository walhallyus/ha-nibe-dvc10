"""NIBE DVC 10 UDP Protocol Handler."""
from __future__ import annotations

import asyncio
import logging
import socket
from dataclasses import dataclass
from typing import Any

from .const import (
    BASE_SEND_HEX,
    CMD_AIRFLOW_IN,
    CMD_AIRFLOW_OUT,
    CMD_AIRFLOW_RECOVERY,
    CMD_FAN_HIGH,
    CMD_FAN_LOW,
    CMD_FAN_MEDIUM,
    CMD_GET_STATUS,
    CMD_TOGGLE_DAYNIGHT,
    CMD_TOGGLE_ONOFF,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    POS_AIRFLOW,
    POS_FAN_SPEED,
    POS_MANUAL_SPEED,
    POS_MODE,
    POS_POWER,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class DVC10Status:
    """Represents the status of a NIBE DVC 10 unit."""

    is_on: bool
    mode: int  # 0=Day, 1=Night, 2=Party
    fan_speed: int  # 1=Low, 2=Medium, 3=High, 4=Manual
    manual_speed_percent: int  # 9-100%
    airflow: int  # 0=Out, 1=Recovery, 2=In
    raw_data: bytes | None = None

    @classmethod
    def from_response(cls, data: bytes) -> "DVC10Status":
        """Parse status from UDP response."""
        if len(data) < 36:
            raise ValueError(f"Invalid response length: {len(data)}")

        # Convert manual speed byte to percentage (0x00=9%, 0xFF=100%)
        manual_byte = data[POS_MANUAL_SPEED]
        manual_percent = int(9 + (manual_byte / 255) * 91)

        return cls(
            is_on=data[POS_POWER] == 1,
            mode=data[POS_MODE],
            fan_speed=data[POS_FAN_SPEED],
            manual_speed_percent=manual_percent,
            airflow=data[POS_AIRFLOW],
            raw_data=data,
        )


class NibeDVC10Protocol:
    """UDP protocol handler for NIBE DVC 10."""

    def __init__(self, host: str, port: int = DEFAULT_PORT, timeout: float = DEFAULT_TIMEOUT):
        """Initialize the protocol handler."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self._lock = asyncio.Lock()

    async def _send_command(self, command_hex: str) -> bytes:
        """Send a UDP command and return the response."""
        full_command = BASE_SEND_HEX + command_hex
        command_bytes = bytes.fromhex(full_command)

        loop = asyncio.get_event_loop()

        def _sync_send() -> bytes:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            try:
                sock.sendto(command_bytes, (self.host, self.port))
                data, _ = sock.recvfrom(4096)
                return data
            finally:
                sock.close()

        async with self._lock:
            return await loop.run_in_executor(None, _sync_send)

    async def get_status(self) -> DVC10Status:
        """Get the current status of the unit."""
        _LOGGER.debug("Getting status from %s:%d", self.host, self.port)
        data = await self._send_command(CMD_GET_STATUS)
        status = DVC10Status.from_response(data)
        _LOGGER.debug("Status: on=%s, mode=%d, fan=%d, airflow=%d",
                      status.is_on, status.mode, status.fan_speed, status.airflow)
        return status

    async def turn_on(self) -> DVC10Status:
        """Turn the unit on."""
        status = await self.get_status()
        if not status.is_on:
            _LOGGER.debug("Turning on %s", self.host)
            data = await self._send_command(CMD_TOGGLE_ONOFF)
            return DVC10Status.from_response(data)
        return status

    async def turn_off(self) -> DVC10Status:
        """Turn the unit off."""
        status = await self.get_status()
        if status.is_on:
            _LOGGER.debug("Turning off %s", self.host)
            data = await self._send_command(CMD_TOGGLE_ONOFF)
            return DVC10Status.from_response(data)
        return status

    async def set_fan_speed(self, speed: int) -> DVC10Status:
        """Set fan speed (1=Low, 2=Medium, 3=High)."""
        status = await self.get_status()
        if status.fan_speed != speed:
            cmd_map = {1: CMD_FAN_LOW, 2: CMD_FAN_MEDIUM, 3: CMD_FAN_HIGH}
            if speed not in cmd_map:
                raise ValueError(f"Invalid fan speed: {speed}")
            _LOGGER.debug("Setting fan speed to %d on %s", speed, self.host)
            data = await self._send_command(cmd_map[speed])
            return DVC10Status.from_response(data)
        return status

    async def set_mode(self, mode: int) -> DVC10Status:
        """Set mode (0=Day, 1=Night). Party mode not directly settable."""
        status = await self.get_status()
        # Toggle day/night - protocol only supports toggle, not direct set
        if mode == 0 and status.mode != 0:  # Want Day, not in Day
            _LOGGER.debug("Setting mode to Day on %s", self.host)
            data = await self._send_command(CMD_TOGGLE_DAYNIGHT)
            return DVC10Status.from_response(data)
        elif mode == 1 and status.mode != 1:  # Want Night, not in Night
            _LOGGER.debug("Setting mode to Night on %s", self.host)
            data = await self._send_command(CMD_TOGGLE_DAYNIGHT)
            return DVC10Status.from_response(data)
        return status

    async def set_airflow(self, airflow: int) -> DVC10Status:
        """Set airflow mode (0=Out, 1=Recovery, 2=In)."""
        status = await self.get_status()
        if status.airflow != airflow:
            cmd_map = {0: CMD_AIRFLOW_OUT, 1: CMD_AIRFLOW_RECOVERY, 2: CMD_AIRFLOW_IN}
            if airflow not in cmd_map:
                raise ValueError(f"Invalid airflow mode: {airflow}")
            _LOGGER.debug("Setting airflow to %d on %s", airflow, self.host)
            data = await self._send_command(cmd_map[airflow])
            return DVC10Status.from_response(data)
        return status
