"""DataUpdateCoordinator for NIBE DVC 10."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL
from .protocol import DVC10Status, NibeDVC10Protocol

_LOGGER = logging.getLogger(__name__)


class NibeDVC10Coordinator(DataUpdateCoordinator[DVC10Status]):
    """Coordinator to manage data updates for NIBE DVC 10."""

    def __init__(self, hass: HomeAssistant, host: str, name: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"NIBE DVC 10 {name}",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        self.host = host
        self.device_name = name
        self.protocol = NibeDVC10Protocol(host)

    async def _async_update_data(self) -> DVC10Status:
        """Fetch data from the device."""
        try:
            return await self.protocol.get_status()
        except TimeoutError as err:
            raise UpdateFailed(f"Timeout communicating with {self.host}") from err
        except OSError as err:
            raise UpdateFailed(f"Error communicating with {self.host}: {err}") from err

    async def async_turn_on(self) -> None:
        """Turn the unit on."""
        self.data = await self.protocol.turn_on()
        self.async_set_updated_data(self.data)

    async def async_turn_off(self) -> None:
        """Turn the unit off."""
        self.data = await self.protocol.turn_off()
        self.async_set_updated_data(self.data)

    async def async_set_fan_speed(self, speed: int) -> None:
        """Set the fan speed."""
        self.data = await self.protocol.set_fan_speed(speed)
        self.async_set_updated_data(self.data)

    async def async_set_mode(self, mode: int) -> None:
        """Set the operating mode."""
        self.data = await self.protocol.set_mode(mode)
        self.async_set_updated_data(self.data)

    async def async_set_airflow(self, airflow: int) -> None:
        """Set the airflow direction."""
        self.data = await self.protocol.set_airflow(airflow)
        self.async_set_updated_data(self.data)

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info for this unit."""
        return {
            "identifiers": {(DOMAIN, self.host)},
            "name": self.device_name,
            "manufacturer": "NIBE",
            "model": "DVC 10",
            "sw_version": "2.0.1",
        }
