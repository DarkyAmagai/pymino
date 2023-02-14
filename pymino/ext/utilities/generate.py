from hmac import new
from hashlib import sha1
from base64 import b64encode
from secrets import token_hex

def device_id() -> str:
    """
    `generate_device_id` Generates a device ID based on a specific string.

    `**Returns**`
    - `str` - Returns a device ID as a string.
    """
    encoded_data = sha1(str(token_hex(20)).encode('utf-8')).hexdigest()

    digest = new(
        b"\xe70\x9e\xcc\tS\xc6\xfa`\x00['e\xf9\x9d\xbb\xc9e\xc8\xe9",
        b"\x19" + bytes.fromhex(encoded_data),
        sha1).hexdigest()

    return f"19{encoded_data}{digest}".upper()

def generate_signature(data: str) -> str:
    """
    `generate_signature` Generates a signature based on a specific string.
    
    `**Parameters**`
    - `data` - Data to generate a signature from
    `**Returns**`
    - `str` - Returns a signature as a string.
    """
    signature = [ 0x19 ]

    signature.extend(new(
        b'\xdf\xa5\xed\x19-\xdan\x88\xa1/\xe1!0\xdcb\x06\xb1%\x1eD',
        data.encode("utf-8"), sha1).digest())

    return b64encode(bytes(signature)).decode("utf-8")