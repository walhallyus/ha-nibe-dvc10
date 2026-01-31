"""Switch platform for NIBE DVC 10."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NibeDVC10Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NIBE DVC 10 switch from a config entry."""
    coordinator: NibeDVC10Coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([NibeDVC10Switch(coordinator)])


class NibeDVC10Switch(CoordinatorEntity[NibeDVC10Coordinator], SwitchEntity):
    """Representation of a NIBE DVC 10 power switch."""

    _attr_has_entity_name = True
    _attr_name = "Power"

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_switch"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.async_turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.async_turn_off()
