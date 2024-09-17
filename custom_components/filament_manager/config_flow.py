import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class FilamentManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Filament Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Appeler la fonction pour créer le filament
            await self._create_filament(self.hass, user_input)
            return self.async_create_entry(title=user_input["name"], data=user_input)

        # Définir le schéma pour les champs à remplir par l'utilisateur
        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("filament_type"): vol.In(["PLA", "ABS", "PETG", "Nylon"]),
            vol.Required("color"): str,
            vol.Required("stock", default=1000): int,
            vol.Required("brand"): str,
            vol.Required("product_link"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def _create_filament(self, hass: HomeAssistant, user_input):
        """Crée un nouveau filament via la config flow."""
        name = user_input["name"]
        filament_type = user_input["filament_type"]
        color = user_input["color"]
        stock = user_input["stock"]
        brand = user_input["brand"]
        product_link = user_input["product_link"]

        # Utiliser async_set pour s'assurer que l'entité est correctement ajoutée
        hass.states.async_set(f"{DOMAIN}.filament_{name.lower().replace(' ', '_')}", stock, {
            "name": name,
            "type": filament_type,
            "color": color,
            "brand": brand,
            "product_link": product_link,
        })
