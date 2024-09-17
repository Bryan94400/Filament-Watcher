from homeassistant.helpers.entity import Entity

class FilamentStockSensor(Entity):
    """Capteur pour suivre le stock de filament."""

    def __init__(self, name, filament_type, initial_stock):
        """Initialise le capteur."""
        self._name = name
        self._filament_type = filament_type
        self._stock = initial_stock

    @property
    def name(self):
        """Nom du capteur."""
        return self._name

    @property
    def state(self):
        """Retourne l'état actuel (le stock)."""
        return self._stock

    @property
    def unit_of_measurement(self):
        """Unité de mesure (grammes)."""
        return "g"

    def update_stock(self, new_stock):
        """Mise à jour du stock."""
        self._stock = new_stock
        self.schedule_update_ha_state()
