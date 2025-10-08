from app.core.scheduler import elevator_scheduler


class TestElevatorAPI:

    def test_call_elevator_success(self, client):
        response = client.post("/call", json={"floor": 5})

        assert response.status_code == 200
        data = response.json()
        assert "Лифт вызван на 5 этаж" in data["message"]
        assert "Вызов принят" in data["status"]

    def test_select_floor_success(self, client):
        elevator_scheduler.current_floor = 3
        elevator_scheduler.current_call_floor = 3
        elevator_scheduler.is_moving = False

        response = client.post("/select", json={"floor": 7})

        assert response.status_code == 200
        data = response.json()
        assert "Этаж 7 добавлен в маршрут" in data["message"]
        assert "Вы выбрали этаж" in data["status"]

    def test_select_floor_when_moving(self, client):
        elevator_scheduler.is_moving = True
        elevator_scheduler.current_floor = 3
        elevator_scheduler.current_call_floor = 3

        response = client.post("/select", json={"floor": 5})

        assert response.status_code == 418

    def test_get_status(self, client):
        elevator_scheduler.queue = [3, 5, 7]
        elevator_scheduler.current_floor = 1
        elevator_scheduler.is_moving = False
        elevator_scheduler.direction = elevator_scheduler.direction.IDLE

        response = client.get("/status")

        assert response.status_code == 200
        data = response.json()
        assert "floor" in data
        assert "direction" in data
        assert "status" in data
        assert "route" in data
        assert data["route"] == [3, 5, 7]
