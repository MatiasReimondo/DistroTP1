def test_domain_fiuba(client):
    response = client.get("/api/domains/fi.uba.ar")

    assert "ip" in response.json
    assert "domain" in response.json
    assert "custom" in response.json
    assert response.status_code == 200


def test_domain_fiuba_not_custom(client):
    response = client.get("/api/domains/fi.uba.ar")

    assert response.json['custom'] is False


def test_domain_not_found(client):
    response = client.get("/api/domains/notfound.uba.ar")
    assert response.status_code == 404


def test_domain_not_found_empty_body(client):
    response = client.get("/api/domains/notfound.uba.ar")
    assert response.json == {}
