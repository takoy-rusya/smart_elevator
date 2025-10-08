import asyncio
from typing import List
from app.models.dto import Direction


class ElevatorScheduler:

    def __init__(self):
        self.current_floor = 1
        self.direction = Direction.IDLE
        self.is_moving = False
        self.queue: List[int] = []
        self.current_call_floor: int = 1

    async def add_call(self, floor: int):
        if floor not in self.queue:
            self.queue.append(floor)
            self.queue.sort()
            await self._start_movement()

    async def add_destination(self, floor: int) -> bool:
        if not self.is_moving and self.current_floor == self.current_call_floor:
            if floor not in self.queue:
                self.queue.append(floor)
                self.queue.sort()
                await self._start_movement()
            return True
        return False

    async def _start_movement(self):
        if not self.is_moving and self.queue:
            asyncio.create_task(self._movement_loop())

    async def _movement_loop(self):
        self.is_moving = True

        while self.queue:
            target_floor = min(self.queue, key=lambda x: abs(x - self.current_floor))
            self.queue.remove(target_floor)

            await self._move_to_floor(target_floor)

            self.current_call_floor = self.current_floor
            await asyncio.sleep(5)

        self.direction = Direction.IDLE
        self.is_moving = False

    async def _move_to_floor(self, target_floor: int):
        self.direction = Direction.UP if target_floor > self.current_floor else Direction.DOWN

        while self.current_floor != target_floor:
            await asyncio.sleep(2)
            if self.direction == Direction.UP:
                self.current_floor += 1
            else:
                self.current_floor -= 1

    def get_status(self):
        return {
            "current_floor": self.current_floor,
            "direction": self.direction,
            "is_moving": self.is_moving,
            "route": self.queue,
        }


elevator_scheduler = ElevatorScheduler()