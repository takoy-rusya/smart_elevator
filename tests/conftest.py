import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.scheduler import elevator_scheduler


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_elevator():
    elevator_scheduler.current_floor = 1
    elevator_scheduler.direction = elevator_scheduler.direction.IDLE
    elevator_scheduler.is_moving = False
    elevator_scheduler.queue.clear()
    elevator_scheduler.current_call_floor = 1

    yield
