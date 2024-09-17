import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.config_entries import ConfigEntry
from datetime import datetime

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

    # Ensure the URL starts with http:// or https://
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

    # Capteur pour le lien d'achat
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

    # Capteur pour la marque
    hass.states.async_set(f"sensor.filament_{name.lower()}_brand", brand, {
        "friendly_name": "Marque",
        "icon": "mdi:tag-text-outline"
    })

    # Capteur pour la quantité totale utilisée
    total_used = 0
    hass.states.async_set(f"sensor.filament_{name.lower()}_total_used", total_used, {
        "friendly_name": "Quantité totale utilisée",
        "unit_of_measurement": "g",
        "icon": "mdi:chart-bar"
    })

    # Créer l'entité `input_number` pour ajuster la quantité actuelle via l'interface utilisateur
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
    hass.states.async_set(input_number_entity_id, stock, input_number_config)

    # Capteur pour la dernière modification
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hass.states.async_set(f"sensor.filament_{name.lower()}_last_updated", last_updated, {
        "friendly_name": "Dernière modification",
        "device_class": "timestamp",
        "icon": "mdi:clock"
    })

    # Utilisation du service input_number pour ajuster la valeur
    async def set_filament_stock(value):
        await hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": input_number_entity_id, "value": value},
            blocking=True,
        )

    return True
