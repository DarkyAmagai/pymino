from hmac import new
from hashlib import sha1
from base64 import b64encode
from secrets import token_hex
from typing import Union


class Generator:
    def __init__(
        self,
        prefix:        Union[str, int],
        device_key:    str,
        signature_key: str
        ) -> None:
        self.PREFIX = bytes.fromhex(str(prefix))
        self.DEVICE_KEY = bytes.fromhex(device_key)
        self.SIGNATURE_KEY = bytes.fromhex(signature_key)

    def device_id(self) -> str:
        """
        `generate_device_id` Generates a device ID based on a specific string.

        `**Returns**`
        - `str` - Returns a device ID as a string.
        """
        encoded_data = sha1(str(token_hex(20)).encode('utf-8')).hexdigest()

        digest = new(
            self.DEVICE_KEY,
            self.PREFIX + bytes.fromhex(encoded_data),
            sha1).hexdigest()

        return f"{bytes.hex(self.PREFIX)}{encoded_data}{digest}".upper()

    def signature(self, data: str) -> str:
        """
        `signature` Generates a signature based on a specific string.
        
        `**Parameters**`
        - `data` - Data to generate a signature from
        `**Returns**`
        - `str` - Returns a signature as a string.
        """

        signature = [self.PREFIX[0]]  
        signature.extend(new(
            self.SIGNATURE_KEY,
            str(data).encode("utf-8"), sha1).digest())

        return b64encode(bytes(signature)).decode("utf-8")