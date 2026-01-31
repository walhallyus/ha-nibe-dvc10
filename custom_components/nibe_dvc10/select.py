"""Select platform for NIBE DVC 10."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    AIRFLOW_DISPLAY_NAMES,
    AIRFLOW_IN,
    AIRFLOW_OUT,
    AIRFLOW_RECOVERY,
    DOMAIN,
    MODE_DAY,
    MODE_NAMES,
    MODE_NIGHT,
    MODE_PARTY,
)
from .coordinator import NibeDVC10Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NIBE DVC 10 select entities from a config entry."""
    coordinator: NibeDVC10Coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        NibeDVC10ModeSelect(coordinator),
        NibeDVC10AirflowSelect(coordinator),
    ])


class NibeDVC10ModeSelect(CoordinatorEntity[NibeDVC10Coordinator], SelectEntity):
    """Representation of NIBE DVC 10 mode selector."""

    _attr_has_entity_name = True
    _attr_name = "Mode"
    _attr_options = ["Day", "Night"]
    _attr_icon = "mdi:weather-sunny"

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_mode"
        self._attr_device_info = coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current mode."""
        if self.coordinator.data is None:
            return None
        mode = self.coordinator.data.mode
        if mode == MODE_DAY:
            return "Day"
        elif mode == MODE_NIGHT:
            return "Night"
        elif mode == MODE_PARTY:
            return "Party"  # Read-only, can't be selected
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the mode."""
        mode_map = {"Day": MODE_DAY, "Night": MODE_NIGHT}
        if option in mode_map:
            await self.coordinator.async_set_mode(mode_map[option])


class NibeDVC10AirflowSelect(CoordinatorEntity[NibeDVC10Coordinator], SelectEntity):
    """Representation of NIBE DVC 10 airflow direction selector."""

    _attr_has_entity_name = True
    _attr_name = "Airflow Direction"
    _attr_options = ["One-way Out [→→]", "Two-way Recovery [←→]", "One-way In [←←]"]
    _attr_icon = "mdi:air-filter"

    def __init__(self, coordinator: NibeDVC10Coordinator) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_airflow"
        self._attr_device_info = coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current airflow direction."""
        if self.coordinator.data is None:
            return None
        airflow = self.coordinator.data.airflow
        return AIRFLOW_DISPLAY_NAMES.get(airflow)

    async def async_select_option(self, option: str) -> None:
        """Change the airflow direction."""
        option_map = {
            "One-way Out [→→]": AIRFLOW_OUT,
            "Two-way Recovery [←→]": AIRFLOW_RECOVERY,
            "One-way In [←←]": AIRFLOW_IN,
        }
        if option in option_map:
            await self.coordinator.async_set_airflow(option_map[option])
