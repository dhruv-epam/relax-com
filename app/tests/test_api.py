import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session, select, SQLModel
from app.models.models import Room, Reservation, RoomType
from app.services.services import engine, init_db
from datetime import date, timedelta

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Drop and recreate all tables for a clean state
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    # Pre-populate rooms
    with Session(engine) as session:
        session.add_all([
            Room(description="Cozy single room", type=RoomType.NORMAL, num_beds=1, max_guests=1),
            Room(description="Spacious double room", type=RoomType.AC, num_beds=2, max_guests=3),
            Room(description="Family suite", type=RoomType.AC, num_beds=3, max_guests=5),
        ])
        session.commit()
    yield
    # Optionally, drop tables after test
    SQLModel.metadata.drop_all(engine)

def test_room_list():
    response = client.get("/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_create_reservation():
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        payload = {
            "guest_details": {
                "name": "John Doe",
                "age": 30,
                "gender": "Male",
                "govt_id": "ID1234",
                "email": "john@example.com",
                "phone": "1234567890"
            },
            "check_in_date": str(date.today()),
            "check_out_date": str(date.today() + timedelta(days=2)),
            "room_id": room.room_id,
            "price_per_day": 1000.0,
            "payments": [
                {"instrument_id": "PAY123", "amount": 2020.0, "status": "Success"}
            ]
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["room_id"] == room.room_id
        assert data["status"] == "Pending"

def test_reservation_status_update():
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        if not room:
            return
        payload = {
            "guest_details": {
                "name": "Jane Doe",
                "age": 28,
                "gender": "Female",
                "govt_id": "ID5678",
                "email": "jane@example.com",
                "phone": "0987654321"
            },
            "check_in_date": str(date.today()),
            "check_out_date": str(date.today() + timedelta(days=1)),
            "room_id": room.room_id,
            "price_per_day": 1200.0,
            "payments": [
                {"instrument_id": "PAY456", "amount": 1212.0, "status": "Success"}
            ]
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 201
        reservation_id = response.json()["reservation_id"]
        # Update status from Pending to Booked
        update_payload = {"status": "Booked"}
        response = client.put(f"/reservations/{reservation_id}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["status"] == "Booked"
        # Invalid transition: Booked to Pending
        update_payload = {"status": "Pending"}
        response = client.put(f"/reservations/{reservation_id}", json=update_payload)
        assert response.status_code == 400

def test_create_reservation_same_day_dates():
    """check_out_date == check_in_date should be rejected with 422."""
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        today = date.today()
        payload = {
            "guest_details": {
                "name": "Test User",
                "age": 25,
                "gender": "Male",
                "govt_id": "ID9999",
                "email": "test@example.com",
                "phone": "5555555555",
            },
            "check_in_date": str(today),
            "check_out_date": str(today),
            "room_id": room.room_id,
            "price_per_day": 500.0,
            "payments": [],
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 422


def test_create_reservation_checkout_before_checkin():
    """check_out_date < check_in_date should be rejected with 422."""
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        today = date.today()
        payload = {
            "guest_details": {
                "name": "Test User",
                "age": 25,
                "gender": "Male",
                "govt_id": "ID9999",
                "email": "test@example.com",
                "phone": "5555555555",
            },
            "check_in_date": str(today + timedelta(days=2)),
            "check_out_date": str(today),
            "room_id": room.room_id,
            "price_per_day": 500.0,
            "payments": [],
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 422


def test_create_reservation_invalid_price():
    """price_per_day <= 0 should be rejected with 422."""
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        today = date.today()
        payload = {
            "guest_details": {
                "name": "Test User",
                "age": 25,
                "gender": "Male",
                "govt_id": "ID9999",
                "email": "test@example.com",
                "phone": "5555555555",
            },
            "check_in_date": str(today),
            "check_out_date": str(today + timedelta(days=1)),
            "room_id": room.room_id,
            "price_per_day": 0.0,
            "payments": [],
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 422


def test_create_reservation_negative_payment():
    """Negative payment amount should be rejected with 422."""
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        today = date.today()
        payload = {
            "guest_details": {
                "name": "Test User",
                "age": 25,
                "gender": "Male",
                "govt_id": "ID9999",
                "email": "test@example.com",
                "phone": "5555555555",
            },
            "check_in_date": str(today),
            "check_out_date": str(today + timedelta(days=1)),
            "room_id": room.room_id,
            "price_per_day": 500.0,
            "payments": [{"instrument_id": "PAY_NEG", "amount": -100.0, "status": "Pending"}],
        }
        response = client.post("/reservations", json=payload)
        assert response.status_code == 422


def test_create_reservation_room_unavailable_returns_409():
    """Booking an already-reserved room should return 409 Conflict."""
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.is_available == True)).first()
        assert room is not None
        today = date.today()
        payload = {
            "guest_details": {
                "name": "First Guest",
                "age": 30,
                "gender": "Male",
                "govt_id": "ID1111",
                "email": "first@example.com",
                "phone": "1111111111",
            },
            "check_in_date": str(today),
            "check_out_date": str(today + timedelta(days=2)),
            "room_id": room.room_id,
            "price_per_day": 800.0,
            "payments": [],
        }
        # First booking succeeds
        response = client.post("/reservations", json=payload)
        assert response.status_code == 201

        # Second booking of the same room returns 409
        payload["guest_details"]["name"] = "Second Guest"
        payload["guest_details"]["email"] = "second@example.com"
        response = client.post("/reservations", json=payload)
        assert response.status_code == 409
