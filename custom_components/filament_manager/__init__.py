import logging
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager et enregistrer chaque filament en tant qu'appareil avec ses attributs."""
    
    # Vérification initiale au démarrage
    await check_for_updates(hass)

    # Récupérer le device_registry et entity_registry pour gérer les appareils et entités
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    # Exemple de création d'un filament enregistré comme appareil
    # Assurons-nous d'inclure tous les attributs
    filament_name = "Wanhao Blanc"  # Remplacer par la variable appropriée
    filament_type = "PLA"            # Exemple d'attribut
    stock = 1200                     # Quantité actuelle en grammes
    brand = "Filament Premium"       # Marque
    product_link = "https://example.com/product-link"  # Lien du produit

    # Enregistrer le filament comme appareil
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, filament_name.lower().replace(' ', '_'))},  # ID unique pour l'appareil
        manufacturer=brand,
        model=filament_type,
        name=filament_name,
        sw_version="1.0",
        configuration_url=product_link,  # Lien direct vers le produit
        via_device=(DOMAIN, filament_name.lower().replace(' ', '_'))
    )

    # Créer l'entité associée avec les attributs spécifiques
    entity_registry.async_get_or_create(
        DOMAIN, "filament_manager", filament_name.lower().replace(' ', '_'),
        suggested_object_id=f"filament_{filament_name.lower().replace(' ', '_')}",
        device_id=device_registry.async_get_device(identifiers={(DOMAIN, filament_name.lower().replace(' ', '_'))}).id,
        config_entry=entry
    )

    # Définir les attributs supplémentaires
    hass.states.async_set(f"{DOMAIN}.filament_{filament_name.lower().replace(' ', '_')}", stock, {
        "name": filament_name,
        "type": filament_type,
        "stock": stock,
        "brand": brand,
        "product_link": product_link,
    })

    return True

async def check_for_updates(hass: HomeAssistant):
    """Vérifie si une mise à jour est disponible."""
    # Logic for checking updates
