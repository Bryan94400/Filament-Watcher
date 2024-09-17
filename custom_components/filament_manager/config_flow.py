import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN  # Si tu utilises un fichier constants.py

@callback
def configured_instances(hass):
    """Returns a list of configured instances."""
    return set(entry.title for entry in hass.config_entries.async_entries(DOMAIN))

class FilamentManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Filament Manager."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # On pourrait vérifier ici les entrées utilisateurs si besoin
            return self.async_create_entry(title="Filament Manager", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("track_filament_usage", default=True): bool,
                vol.Required("low_filament_threshold", default=10): vol.Coerce(int),
            }),
            errors=errors,
        )
