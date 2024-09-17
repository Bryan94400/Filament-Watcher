from .sensor import FilamentStockSensor
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup Filament Manager via YAML."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager via l'interface graphique."""
    # Créer un capteur de stock pour un filament PLA avec un stock initial de 1000 g
    stock_sensor = FilamentStockSensor("Stock Filament PLA", "PLA", 1000)
    hass.states.async_set(f"{DOMAIN}.filament_stock_pla", stock_sensor.state, {
        "unit_of_measurement": stock_sensor.unit_of_measurement
    })
    
    return True
