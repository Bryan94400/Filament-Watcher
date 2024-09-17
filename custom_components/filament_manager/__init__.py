from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the filament sensors."""
    sensors = []
    sensors.append(FilamentSensor("Filament Color", "blue", 5))  # Exemple de capteur
    async_add_entities(sensors)

class FilamentSensor(Entity):
    """Representation of a filament sensor."""

    def __init__(self, name, color, quantity):
        self._name = name
        self._color = color
        self._quantity = quantity

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} ({self._color})"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._quantity

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return "mdi:printer-3d"  # Choisis une icône appropriée
