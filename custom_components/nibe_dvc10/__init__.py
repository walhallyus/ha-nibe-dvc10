"""NIBE DVC 10 Heat Recovery Ventilation Integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import NibeDVC10Coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.FAN, Platform.SELECT, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NIBE DVC 10 from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = NibeDVC10Coordinator(
        hass,
        host=entry.data[CONF_HOST],
        name=entry.data.get(CONF_NAME, f"NIBE DVC 10 {entry.data[CONF_HOST]}"),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
