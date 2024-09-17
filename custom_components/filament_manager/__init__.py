import logging
import aiohttp
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/repos/ton_nom_utilisateur_github/Filament-Watcher/releases/latest"
CURRENT_VERSION = "1.0.0"  # Version actuelle de ton plugin

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
                        hass.components.persistent_notification.create(
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

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager et planifie la vérification des mises à jour."""
    
    # Vérification initiale au démarrage
    await check_for_updates(hass)
    
    # Planifie la vérification toutes les 5 minutes
    async_track_time_interval(hass, check_for_updates, timedelta(minutes=5))
    
    return True
