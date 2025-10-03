

async def test_get_me(ac):
    response = await ac.get("/auth/me")
    assert response
    assert response.status_code == 200
    print(f"{response.json()=}")