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


def test_create_new_custom_domain_status_code(client):
    response = client.post('/api/custom-domains',
                           json={'domain': 'custom.domain.com',
                                 'ip': '1.1.1.1'})

    assert response.status_code == 201


def test_create_new_custom_domain_body(client):
    response = client.post('/api/custom-domains',
                           json={'domain': 'custom.domain.com',
                                 'ip': '1.1.1.1'})

    assert response.json['domain'] == 'custom.domain.com'
    assert response.json['ip'] == '1.1.1.1'
    assert response.json['custom'] is True


def test_create_new_custom_domain_no_ip(client):
    response = client.post('/api/custom-domains',
                           json={'domain': 'custom.domain.com'})
    assert response.status_code == 400
    assert response.json == {}


def test_create_new_custom_domain_no_domain(client):
    response = client.post('/api/custom-domains',
                           json={'ip': '1.1.1.1'})
    assert response.status_code == 400
    assert response.json == {}


def test_create_new_custom_domain_already_exists(client):
    client.post('/api/custom-domains',
                json={'domain': 'custom.domain.com',
                      'ip': '1.1.1.1'})

    response = client.post('/api/custom-domains',
                           json={'domain': 'custom.domain.com',
                                 'ip': '2.2.2.2'})
    assert response.status_code == 400
    assert response.json == {}
