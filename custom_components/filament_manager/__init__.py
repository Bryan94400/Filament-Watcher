import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_component import EntityComponent
from datetime import datetime
from homeassistant.components.input_number import (
    async_set_value,
    DOMAIN as INPUT_NUMBER_DOMAIN,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Filament Manager with provided user information."""

    user_input = entry.data
    name = user_input["name"]
    filament_type = user_input["filament_type"]
    stock = user_input["stock"]
    brand = user_input["brand"]
    product_link = user_input["product_link"]

    if not product_link.startswith(("http://", "https://")):
        product_link = "https://" + product_link

    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, name.lower().replace(' ', '_'))},
        manufacturer=brand,
        model=filament_type,
        name=name,
        sw_version="1.0",
        configuration_url=product_link,
    )

    # Création du capteur pour le lien d'achat
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_link",
        suggested_object_id=f"filament_{name.lower()}_link",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_link", product_link, {
        "friendly_name": "Lien d'achat",
        "icon": "mdi:link",
        "custom_ui_more_info": {
            "tap_action": {
                "action": "url",
                "url_path": product_link
            }
        }
    })

    # Création du capteur pour la marque
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_brand",
        suggested_object_id=f"filament_{name.lower()}_brand",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_brand", brand, {
        "friendly_name": "Marque",
        "icon": "mdi:tag-text-outline"
    })

    # Création du capteur pour la quantité totale utilisée
    total_used = 0
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_total_used",
        suggested_object_id=f"filament_{name.lower()}_total_used",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_total_used", total_used, {
        "friendly_name": "Quantité totale utilisée",
        "unit_of_measurement": "g",
        "icon": "mdi:chart-bar"
    })

    # Configuration d'`input_number` pour ajuster la quantité actuelle
    input_number_entity_id = f"input_number.filament_{name.lower()}_stock"
    input_number_config = {
        "min": 0,
        "max": 10000,
        "step": 1,
        "mode": "box",
        "name": f"Stock de {name}",
        "unit_of_measurement": "g",
        "icon": "mdi:weight"
    }

    # Créer l'entité `input_number` pour la gestion du stock
    hass.states.async_set(input_number_entity_id, stock, input_number_config)

    # Date de dernière modification
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_last_updated",
        suggested_object_id=f"filament_{name.lower()}_last_updated",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_last_updated", last_updated, {
        "friendly_name": "Dernière modification",
        "device_class": "timestamp",
        "icon": "mdi:clock"
    })

    return True
