from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

PLATFORMS = ["button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault("routeros_recovery", {})[entry.entry_id] = entry.data
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
