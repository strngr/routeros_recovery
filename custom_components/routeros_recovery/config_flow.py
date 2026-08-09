import voluptuous as vol
from homeassistant import config_entries

class RouterOSRecoveryFlow(config_entries.ConfigFlow, domain="routeros_recovery"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="RouterOS Recovery", data=user_input)

        schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional("api_port", default=8728): int,
            vol.Optional("ssh_port", default=22): int,
            vol.Required("dst_port"): str,
            vol.Required("to_address"): str,
            vol.Required("to_port"): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
