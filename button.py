import logging
import socket

from homeassistant.components.button import ButtonEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([RestoreForwardButton(entry.data)])


class RestoreForwardButton(ButtonEntity):
    _attr_name = "Restore MikroTik port forward"

    def __init__(self, cfg):
        self._cfg = cfg

    def press(self) -> None:
        try:
            self._via_api()
            _LOGGER.info("NAT rule added via RouterOS API")
        except Exception as api_err:
            _LOGGER.warning("API path failed (%s), falling back to SSH", api_err)
            try:
                self._via_ssh()
                _LOGGER.info("NAT rule added via SSH")
            except Exception as ssh_err:
                _LOGGER.error("SSH fallback also failed: %s", ssh_err)
                raise

    # ---------- API path ----------
    def _via_api(self):
        import librouteros

        api = librouteros.connect(
            host=self._cfg["host"],
            username=self._cfg["username"],
            password=self._cfg["password"],
            port=self._cfg.get("api_port", 8728),
            timeout=5,
        )
        nat = api.path("ip", "firewall", "nat")
        nat.add(
            chain="dstnat",
            protocol="tcp",
            **{"dst-port": self._cfg["dst_port"]},
            action="dst-nat",
            **{"to-addresses": self._cfg["to_address"], "to-ports": self._cfg["to_port"]},
        )

    # ---------- SSH path ----------
    def _via_ssh(self):
        import paramiko

        cmd = (
            "/ip firewall nat add chain=dstnat protocol=tcp "
            f"dst-port={self._cfg['dst_port']} action=dst-nat "
            f"to-addresses={self._cfg['to_address']} to-ports={self._cfg['to_port']}"
        )

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=self._cfg["host"],
                port=self._cfg.get("ssh_port", 22),
                username=self._cfg["username"],
                password=self._cfg["password"],
                timeout=5,
                look_for_keys=False,
                allow_agent=False,
            )
            stdin, stdout, stderr = client.exec_command(cmd, timeout=5)
            err = stderr.read().decode().strip()
            if err:
                raise RuntimeError(f"RouterOS returned error: {err}")
        finally:
            client.close()
