from base64 import b64encode
from hashlib import sha1
from json import loads
from hmac import new
from os import path
from typing import Optional
from httpx import get
from uuid import uuid4

def generate_device_id(data: Optional[str]=None) -> str:
    """
    `generate_device_id` Generates a device ID based on a specific string.

    `**Example**` `>>> generate_device_id()`

    `**Parameters**`
    - `data` - Data to generate a device ID from

    `**Returns**`
    - `str` - Returns a device ID as a string.

    """
    if data is not None:
        encoded_data = sha1(str(data).encode("utf-8")).digest()
    else:
        encoded_data = sha1(str(uuid4()).encode("utf-8")).digest()
        
    digest = new(
        b'\x02\xb2X\xc65Y\xd8\x80C!\xc5\xd5\x06Z\xf3 5\x8d6o',
        b"\x42" + encoded_data,
        sha1).hexdigest()
    
    return "42" + encoded_data.hex() + digest

def generate_signature(data: str) -> str:
    """
    `generate_signature` Generates a signature based on a specific string.

    `**Example**` `>>> generate_signature("Hello World")`

    `**Parameters**`
    - `data` - Data to generate a signature from

    `**Returns**`
    - `str` - Returns a signature as a string.

    """
    signature = [ 0x42 ]
    signature.extend(new(
        b'\xf8\xe7\xa6\x1a\xc3\xf7%\x94\x1e:\xc7\xca\xe2\xd6\x88\xbe\x97\xf3\x0b\x93',
        str(data).encode("utf-8"), sha1).digest())

    return b64encode(bytes(signature)).decode("utf-8")

def fetch_device() -> str:
    """
    `fetch_device` Fetches a device ID from the API.
    
    `**Example**` `>>> fetch_device()`
    
    `**Parameters**`
    - `None`

    `**Returns**`
    - `str` - Returns a device ID as a string.

    """
    return loads(get("https://humanis.gay/generate/device").text)["deviceID"]

def fetch_signature(data: str) -> str:
    """
    `fetch_signature` Fetches a signature from the API.

    `**Example**` `>>> fetch_signature("Hello World")`

    `**Parameters**`
    - `data` - Data to generate a signature from

    `**Returns**`
    - `str` - Returns a signature as a string.

    """
    return loads(get(f"https://humanis.gay/generate/signature?data={data}").text)["signature"]

def fetch_sessions():
    """
    `fetch_sessions` Fetches the sessions.json file.

    `**Example**` `>>> fetch_sessions()`

    `**Parameters**`
    - `None`

    `**Returns**`
    - `str` - Returns the sessions.json file.

    """
    return path.join(path.dirname(path.realpath(__file__)), "sessions.json")
