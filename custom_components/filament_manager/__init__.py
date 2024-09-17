from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Filament Manager component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Filament Manager from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data
    # Ici, on peut initialiser tout ce qui est nécessaire, par exemple les capteurs ou le suivi de filament
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
