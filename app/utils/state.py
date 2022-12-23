import asyncio
from typing import Any

from pydantic import BaseSettings

semaphore = asyncio.BoundedSemaphore(1)

class State(BaseSettings):

    websockets: dict[str, dict] = {}

state = State()
