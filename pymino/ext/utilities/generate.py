import hmac
import hashlib
import base64
import secrets
from typing import Union

import requests

__all__ = ("Generator",)


class Generator:
    def __init__(
        self,
        prefix: str,
        device_key: str,
        signature_key: str,
        key: str,
    ) -> None:
        self.prefix = bytes.fromhex(prefix)
        self.device_key = bytes.fromhex(device_key)
        self.signature_key = bytes.fromhex(signature_key)
        self.key = key

    def device_id(self) -> str:
        """
        Generates a device ID based on a specific string.

        `**Returns**`
        - `str` - Returns a device ID as a string.
        """
        data = (
            self.prefix + hashlib.sha1(secrets.token_hex(20).encode("utf-8")).digest()
        )
        digest = hmac.new(
            self.device_key,
            data,
            hashlib.sha1,
        ).hexdigest()
        return f"{data.hex()}{digest}".upper()

    def signature(self, data: Union[bytes, str]) -> str:
        """
        Generates a signature based on a specific string.

        `**Parameters**`
        - `data` - Data to generate a signature from
        `**Returns**`
        - `str` - Returns a signature as a string.
        """
        if not isinstance(data, bytes):
            data = data.encode("utf-8")
        signature = [self.prefix[0]]
        signature.extend(hmac.new(self.signature_key, data, hashlib.sha1).digest())
        return base64.b64encode(bytes(signature)).decode("utf-8")

    def update_device(self, device: str) -> str:
        """
        Update a device ID to new prefix.

        :param device: The device ID to update.
        :type device: str
        :return: The updated device ID as a string.
        :rtype: str
        """
        data = (
            self.prefix
            + hashlib.sha1(
                str(
                    bytes.fromhex(device[2:42]),
                ).encode("utf-8")
            ).digest()
        )
        digest = hmac.new(
            self.device_key,
            data,
            hashlib.sha1,
        ).hexdigest()
        return f"{data.hex()}{digest}".upper()

    def ndc_message_signature(self, data: Union[str, bytes], userId: str) -> str:
        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        response = requests.post(
            url="https://app.pymino.site/api/v1/pymino",
            params={
                "user_id": userId,
                "key": self.key,
                "version": "G7P4XQ",
            },
            data=data,
        )
        response.raise_for_status()
        return response.text
