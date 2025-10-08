from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    IDLE = "idle"


class CallRequest(BaseModel):
    floor: int


class SelectRequest(BaseModel):
    floor: int


class CallResponse(BaseModel):
    message: str
    current_floor: int
    status: str


class SelectResponse(BaseModel):
    message: str
    current_floor: int
    status: str


class StatusResponse(BaseModel):
    status: str
    floor: int
    direction: str
    route: List[int]
