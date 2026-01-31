"""Fan platform for NIBE DVC 10."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    FAN_SPEED_HIGH,
    FAN_SPEED_LOW,
    FAN_SPEED_MEDIUM,
    FAN_SPEED_NAMES,
)
from .coordinator import NibeDVC10Coordinator

_LOGGER = logging.getLogger(__name__)

PRESET_MODES = ["low", "medium", "high"]
SPEED_TO_PRESET = {1: "low", 2: "medium", 3: "high"}
PRESET_TO_SPEED = {"low": 1, "medium": 2, "high": 3}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NIBE DVC 10 fan from a config entry."""
    coordinator: NibeDVC10Coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([NibeDVC10Fan(coordinator)])


class NibeDVC10Fan(CoordinatorEntity[NibeDVC10Coordinator], FanEntity):
    """Representation of a NIBE DVC 10 fan."""

    _attr_has_entity_name = True
    _attr_name = "Fan"
    _attr_supported_features = FanEntityFeature.PRESET_MODE | FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the fan."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_fan"
        self._attr_device_info = coordinator.device_info
        self._attr_preset_modes = PRESET_MODES

    @property
    def is_on(self) -> bool | None:
        """Return true if the fan is on."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.is_on

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        if self.coordinator.data is None:
            return None
        speed = self.coordinator.data.fan_speed
        return SPEED_TO_PRESET.get(speed, "low")

    @property
    def percentage(self) -> int | None:
        """Return the current speed percentage."""
        if self.coordinator.data is None:
            return None
        if not self.coordinator.data.is_on:
            return 0
        # Map preset speeds to percentage
        speed = self.coordinator.data.fan_speed
        return {1: 33, 2: 66, 3: 100}.get(speed, 33)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn the fan on."""
        await self.coordinator.async_turn_on()
        if preset_mode:
            await self.async_set_preset_mode(preset_mode)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        await self.coordinator.async_turn_off()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode."""
        if preset_mode in PRESET_TO_SPEED:
            await self.coordinator.async_set_fan_speed(PRESET_TO_SPEED[preset_mode])
