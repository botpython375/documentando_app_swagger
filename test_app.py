from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "API está funcionando"}


def test_login_sucesso():
    client = app.test_client()
    response = client.post("/login", json={
        "email": "user@example.com",
        "senha": "1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_protegido_sem_token():
    client = app.test_client()
    response = client.get("/protegido")
    assert response.status_code == 401


def test_protegido_com_token():
    client = app.test_client()

    login = client.post("/login", json={
        "email": "user@example.com",
        "senha": "1234"
    })
    token = login.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protegido", headers=headers)

    assert response.status_code == 200
    assert "Olá, user@example.com!" in response.get_json()["msg"]
