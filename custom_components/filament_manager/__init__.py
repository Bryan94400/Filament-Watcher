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
    color = user_input["color"]
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

    # Création des entités

    # Entité pour la marque
    hass.states.async_set(f"sensor.filament_{name.lower()}_brand", brand, {
        "friendly_name": "Marque",
        "icon": "mdi:tag-text-outline"
    })

    # Entité pour la couleur
    hass.states.async_set(f"sensor.filament_{name.lower()}_color", color, {
        "friendly_name": "Couleur",
        "icon": "mdi:palette"
    })

    # Entité pour la quantité réelle
    input_number_entity_id = f"input_number.filament_{name.lower()}_stock"
    hass.states.async_set(input_number_entity_id, stock, {
        "friendly_name": f"Quantité réelle de {name}",
        "min": 0,
        "max": 10000,
        "step": 1,
        "unit_of_measurement": "g",
        "icon": "mdi:weight"
    })

    # Entité pour la quantité utilisée
    total_used = 0
    hass.states.async_set(f"sensor.filament_{name.lower()}_total_used", total_used, {
        "friendly_name": "Quantité totale utilisée",
        "unit_of_measurement": "g",
        "icon": "mdi:chart-bar"
    })

    # Entité pour l'URL du produit
    hass.states.async_set(f"sensor.filament_{name.lower()}_url", product_link, {
        "friendly_name": "Lien d'achat",
        "icon": "mdi:link",
        "url": product_link
    })

    # Entité pour la dernière modification
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hass.states.async_set(f"sensor.filament_{name.lower()}_last_used", last_updated, {
        "friendly_name": "Dernière utilisation",
        "device_class": "timestamp",
        "icon": "mdi:clock"
    })

    # Input text pour modifier l'URL directement
    input_text_url_entity_id = f"input_text.filament_{name.lower()}_url"
    hass.states.async_set(input_text_url_entity_id, product_link, {
        "friendly_name": f"URL du fournisseur pour {name}",
        "icon": "mdi:web",
        "mode": "text"
    })

    # Utilisation du service input_number pour ajuster la valeur du stock
    async def set_filament_stock(value):
        await hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": input_number_entity_id, "value": value},
            blocking=True,
        )

    # Utilisation du service input_text pour modifier l'URL
    async def set_filament_url(url):
        await hass.services.async_call(
            "input_text",
            "set_value",
            {"entity_id": input_text_url_entity_id, "value": url},
            blocking=True,
        )

    return True
