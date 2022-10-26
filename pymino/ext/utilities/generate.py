from base64 import b64encode
from contextlib import suppress
from hashlib import sha1
from hmac import new
from typing import Optional, Union, BinaryIO, Callable
from uuid import uuid4
from io import BytesIO
from time import time, sleep as wait
from threading import Thread
from inspect import signature as inspect_signature
from random import randint
from orjson import dumps, loads
from websocket import WebSocket, WebSocketApp, WebSocketConnectionClosedException
from httpx import get
from aiohttp import ClientSession, ClientResponse
from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectorError
from asyncio import Queue, get_event_loop, AbstractEventLoop
from ..entities.messages import *
from ..entities.threads import *
from ..entities.userprofile import *
from ..entities.general import *
from ..entities.wsevents import *

def device_id(data: Optional[str]=None) -> str:
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

def signature(data: str) -> str:
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