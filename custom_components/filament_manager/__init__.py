from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Filament Manager from YAML configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Filament Manager from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data
    # Ici, tu pourrais initialiser d'autres composants comme des capteurs ou des services liés à ton plugin.
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
