"""Sensor platform for NIBE DVC 10."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    AIRFLOW_DISPLAY_NAMES,
    DOMAIN,
    FAN_SPEED_NAMES,
    MODE_NAMES,
)
from .coordinator import NibeDVC10Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NIBE DVC 10 sensors from a config entry."""
    coordinator: NibeDVC10Coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        NibeDVC10StatusSensor(coordinator),
        NibeDVC10FanSpeedSensor(coordinator),
    ])


class NibeDVC10StatusSensor(CoordinatorEntity[NibeDVC10Coordinator], SensorEntity):
    """Representation of NIBE DVC 10 status sensor."""

    _attr_has_entity_name = True
    _attr_name = "Status"
    _attr_icon = "mdi:information"

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_status"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> str | None:
        """Return the status."""
        if self.coordinator.data is None:
            return "Unknown"
        data = self.coordinator.data
        if not data.is_on:
            return "Off"
        mode = MODE_NAMES.get(data.mode, "Unknown")
        return f"On - {mode.capitalize()}"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return {}
        data = self.coordinator.data
        return {
            "power": "On" if data.is_on else "Off",
            "mode": MODE_NAMES.get(data.mode, "Unknown"),
            "fan_speed": FAN_SPEED_NAMES.get(data.fan_speed, "Unknown"),
            "airflow": AIRFLOW_DISPLAY_NAMES.get(data.airflow, "Unknown"),
            "host": self.coordinator.host,
        }


class NibeDVC10FanSpeedSensor(CoordinatorEntity[NibeDVC10Coordinator], SensorEntity):
    """Representation of NIBE DVC 10 fan speed sensor."""

    _attr_has_entity_name = True
    _attr_name = "Fan Speed"
    _attr_icon = "mdi:fan"

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_fan_speed_sensor"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> str | None:
        """Return the fan speed."""
        if self.coordinator.data is None:
            return None
        speed = self.coordinator.data.fan_speed
        return FAN_SPEED_NAMES.get(speed, "Unknown").capitalize()
