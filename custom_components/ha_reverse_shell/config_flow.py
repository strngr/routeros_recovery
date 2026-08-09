import voluptuous as vol
from homeassistant import config_entries

class HAReverseShellFlow(config_entries.ConfigFlow, domain="ha_reverse_shell"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="HA Reverse Shell", data=user_input)

        schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("port", default=31337): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
