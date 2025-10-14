import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-10-07", "2025-10-08", 200),
        (1, "2025-10-07", "2025-10-08", 200),
        (1, "2025-10-07", "2025-10-08", 200),
        (1, "2025-10-07", "2025-10-08", 200),
        (1, "2025-10-07", "2025-10-08", 200),
        (1, "2025-10-07", "2025-10-08", 500),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, item_count",
    [
        (1, "2025-10-07", "2025-10-08", 200, 1),
        (1, "2025-10-07", "2025-10-08", 200, 2),
        (1, "2025-10-07", "2025-10-08", 200, 3),
        (1, "2025-10-07", "2025-10-08", 200, 4),
        (1, "2025-10-07", "2025-10-08", 200, 5),
        (1, "2025-10-07", "2025-10-08", 500, 5),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    status_code,
    item_count,
    db,
    authenticated_ac: AsyncClient,
    clear_books,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response
    assert response.status_code == status_code

    get_response = await authenticated_ac.get("/bookings/me")

    result = get_response.json()
    print(f"{result=}")
    assert item_count == len(result["result"])
