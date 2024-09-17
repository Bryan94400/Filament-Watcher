import logging
import aiohttp
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.persistent_notification import create as create_notification  # Import direct pour éviter la dépréciation
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/repos/Bryan94400/Filament-Watcher/releases/latest"
CURRENT_VERSION = "1.0.0"  # Version actuelle de ton plugin

# Liste des filaments
FILAMENTS = {}

class FilamentEntity(Entity):
    """Représente un filament dans Home Assistant."""

    def __init__(self, name, filament_type, color, stock):
        """Initialisation de l'entité filament."""
        self._name = name
        self._filament_type = filament_type
        self._color = color
        self._stock = stock

    @property
    def name(self):
        """Retourne le nom de l'entité."""
        return self._name

    @property
    def state(self):
        """Retourne le stock actuel du filament."""
        return self._stock

    @property
    def extra_state_attributes(self):
        """Retourne les attributs supplémentaires."""
        return {
            "type": self._filament_type,
            "color": self._color,
        }

    def update_stock(self, new_stock):
        """Mise à jour du stock de filament."""
        self._stock = new_stock
        self.schedule_update_ha_state()

async def check_for_updates(hass: HomeAssistant):
    """Vérifie si une mise à jour est disponible."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(GITHUB_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    latest_version = data["tag_name"]

                    # Comparer les versions
                    if latest_version != CURRENT_VERSION:
                        _LOGGER.info(f"Nouvelle version disponible : {latest_version}")
                        hass.states.async_set(f"{DOMAIN}.update_available", f"Nouvelle version disponible : {latest_version}")
                        create_notification(
                            hass,
                            f"Une nouvelle version de Filament Manager ({latest_version}) est disponible. Mettez à jour votre intégration via HACS.",
                            title="Mise à jour Filament Manager"
                        )
                    else:
                        _LOGGER.info("Aucune mise à jour disponible")
                        hass.states.async_set(f"{DOMAIN}.update_available", "Aucune mise à jour disponible")
                else:
                    _LOGGER.error(f"Erreur lors de la requête HTTP : {response.status}")
                    hass.states.async_set(f"{DOMAIN}.update_available", "Erreur lors de la vérification de la mise à jour")
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la vérification des mises à jour : {e}")
            hass.states.async_set(f"{DOMAIN}.update_available", "Erreur lors de la vérification de la mise à jour")

async def create_filament(hass: HomeAssistant, name: str, filament_type: str, color: str, stock: int):
    """Crée un nouveau filament."""
    # Création de l'entité filament
    filament = FilamentEntity(name, filament_type, color, stock)
    FILAMENTS[name] = filament
    
    # Ajoute le filament dans hass.data
    hass.states.async_set(f"{DOMAIN}.filament_{name}", filament.state, {
        "type": filament._filament_type,
        "color": filament._color,
        "stock": filament._stock
    })
    
    _LOGGER.info(f"Nouveau filament créé : {name} (Type: {filament_type}, Couleur: {color}, Stock: {stock}g)")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager et planifie la vérification des mises à jour."""
    
    # Vérification initiale au démarrage
    await check_for_updates(hass)

    # Planifie la vérification toutes les 5 minutes
    async_track_time_interval(hass, check_for_updates, timedelta(minutes=5))
    
    # Créer un filament par défaut (exemple)
    await create_filament(hass, "PLA_Blanc", "PLA", "Blanc", 1000)
    
    return True
