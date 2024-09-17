import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class FilamentManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Filament Manager."""

    VERSION = 1
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Filament Manager", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("option1", default=True): bool,
            })
        )
