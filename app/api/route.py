from fastapi import APIRouter

from app.api.use_case import (
    call_elevator,
    select_floor,
    status_elevator
)
from app.models.dto import (
    StatusResponse,
    SelectResponse,
    CallResponse
)


def router() -> APIRouter:
    route = APIRouter(tags=["API"])

    route.add_api_route(
        methods=["POST"],
        path="/call",
        endpoint=call_elevator,
        summary="API вызова лифта",
        response_model=CallResponse,
    ),

    route.add_api_route(
        methods=["POST"],
        path="/select",
        endpoint=select_floor,
        summary="API выбора этажа назначения",
        response_model=SelectResponse
    ),

    route.add_api_route(
        methods=["GET"],
        path="/status",
        endpoint=status_elevator,
        summary="API статуса системы",
        response_model=StatusResponse
    )

    return route
