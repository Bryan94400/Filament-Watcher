import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.config_entries import ConfigEntry
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

    # Vérifier que le lien d'achat commence par 'https://' ou 'http://'
    if not product_link.startswith(("http://", "https://")):
        product_link = "https://" + product_link

    # Enregistrer le filament comme appareil
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, name.lower().replace(' ', '_'))},
        manufacturer=brand,
        model=filament_type,
        name=name,
        sw_version="1.0",
        configuration_url=product_link,  # Lien direct vers le produit
    )

    # Réduire la taille des informations pour les rendre plus concises
    hass.states.async_set(f"{DOMAIN}.filament_{name.lower().replace(' ', '_')}", stock, {
        "name": name,
        "type": filament_type,
        "stock": f"{stock} g",
        "brand": brand,
        "product_link": product_link,
        "link_text": "Acheter"  # Remplacer 'Visiter' par 'Acheter'
    })

    # Créer et associer les entités (quantité, marque, etc.) à l'appareil
    # Quantité
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_stock",
        suggested_object_id=f"filament_{name.lower()}_stock",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_stock", stock, {
        "unit_of_measurement": "g",
        "friendly_name": "Stock",
        "device_class": "measurement"
    })

    # Marque
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_brand",
        suggested_object_id=f"filament_{name.lower()}_brand",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_brand", brand, {
        "friendly_name": "Marque",
    })

    # Lien d'achat
    entity_registry.async_get_or_create(
        "sensor", DOMAIN, f"{name}_link",
        suggested_object_id=f"filament_{name.lower()}_link",
        device_id=device.id,
        config_entry=entry
    )
    hass.states.async_set(f"sensor.filament_{name.lower()}_link", product_link, {
        "friendly_name": "Lien d'achat",
    })

    return True

async def check_for_updates(hass: HomeAssistant):
    """Vérifie si une mise à jour est disponible."""
    # Logic to check for updates
    pass
