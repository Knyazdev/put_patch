from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email, password", [("user@example.com", "1234567")])
async def test_register_user(email: str, password: str, ac: AsyncClient):
    register_reponse = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register_reponse
    assert register_reponse.status_code == 200

    login_response = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )

    assert login_response
    assert login_response.status_code == 200

    res = login_response.json()

    assert "access_token" in res
    assert login_response.cookies.get("access_token")

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == 200
    res = response_me.json()

    assert email == res["email"]

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == 400
