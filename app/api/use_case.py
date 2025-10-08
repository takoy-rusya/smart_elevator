from fastapi import HTTPException
from starlette import status

from app.models.dto import (
    CallRequest,
    SelectRequest,
    CallResponse,
    SelectResponse,
    StatusResponse
)
from app.core.scheduler import elevator_scheduler


async def call_elevator(request: CallRequest) -> CallResponse:
    await elevator_scheduler.add_call(request.floor)

    return CallResponse(
        message=f"Лифт вызван на {request.floor} этаж",
        current_floor=elevator_scheduler.current_floor,
        status="Вызов принят"
    )


async def select_floor(request: SelectRequest) -> SelectResponse:
    success = await elevator_scheduler.add_destination(request.floor)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Можно выбирать этаж только когда лифт стоит на этаже вызова")

    return SelectResponse(
        message=f"Этаж {request.floor} добавлен в маршрут",
        current_floor=elevator_scheduler.current_floor,
        status="Вы выбрали этаж"
    )


async def status_elevator() -> StatusResponse:
    stat = elevator_scheduler.get_status()

    return StatusResponse(
        status="moving" if stat["is_moving"] else "Пустой",
        floor=stat["current_floor"],
        direction=stat["direction"],
        route=stat["route"]
    )
