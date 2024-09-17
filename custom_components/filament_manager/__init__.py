import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager en enregistrant les informations fournies par l'utilisateur."""

    # Récupérer les informations de l'entrée (ce que l'utilisateur a fourni)
    user_input = entry.data
    name = user_input["name"]
    filament_type = user_input["filament_type"]
    stock = user_input["stock"]
    brand = user_input["brand"]
    product_link = user_input["product_link"]

    # Récupérer le device_registry et entity_registry pour gérer les appareils et entités
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    # Enregistrer le filament comme appareil
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, name.lower().replace(' ', '_'))},
        manufacturer=brand,
        model=filament_type,
        name=name,
        sw_version="1.0",
        configuration_url=product_link,  # Lien direct vers le produit
    )

    # Créer l'entité associée avec les attributs spécifiques
    entity_registry.async_get_or_create(
        DOMAIN, "filament_manager", name.lower().replace(' ', '_'),
        suggested_object_id=f"filament_{name.lower().replace(' ', '_')}",
        device_id=device_registry.async_get_device(identifiers={(DOMAIN, name.lower().replace(' ', '_'))}).id,
        config_entry=entry
    )

    # Définir les attributs supplémentaires
    hass.states.async_set(f"{DOMAIN}.filament_{name.lower().replace(' ', '_')}", stock, {
        "name": name,
        "type": filament_type,
        "stock": stock,
        "brand": brand,
        "product_link": product_link,
        "link_text": "Acheter"
    })

    return True
