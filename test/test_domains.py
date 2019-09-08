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


def test_created_custom_domains_show_up_in_resolver(client):
    client.post('/api/custom-domains',
                json={'domain': 'custom.domain.com',
                      'ip': '1.1.1.1'})

    response = client.get('/api/domains/custom.domain.com')
    assert response.json['ip'] == '1.1.1.1'
    assert response.json['custom'] is True


def test_modify_domain(client, custom_domain):
    response = client.put(f'/api/custom-domains/{custom_domain.domain}',
                          json={'ip': '1.1.1.1',
                                'domain': 'other.custom.domain.com'})

    assert response.status_code == 200


def test_modify_domain_response(client, custom_domain):
    response = client.put(f'/api/custom-domains/{custom_domain.domain}',
                          json={'ip': '1.1.1.1',
                                'domain': 'other.custom.domain.com'})

    assert response.json['ip'] == '1.1.1.1'
    assert response.json['domain'] == 'other.custom.domain.com'


def test_modify_non_existing_domain(client):
    response = client.put(f'/api/custom-domains/invalid.domain.com',
                          json={'ip': '1.1.1.1',
                                'domain': 'other.custom.domain.com'})
    assert response.status_code == 404


def test_modify_domain_missing_ip(client, custom_domain):
    response = client.put(f'/api/custom-domains/{custom_domain.domain}',
                          json={'domain': 'other.custom.domain.com'})

    assert response.status_code == 400
    assert response.json == {}


def test_modify_domain_missing_domain(client, custom_domain):
    response = client.put(f'/api/custom-domains/{custom_domain.domain}',
                          json={'ip': '1.1.1.1'})
    assert response.status_code == 400
    assert response.json == {}


def test_modified_domain_shows_in_get(client, custom_domain):
    put_response = client.put(f'/api/custom-domains/{custom_domain.domain}',
                              json={'domain': 'other.custom.domain.com',
                                    'ip': '2.2.2.2'})

    assert put_response.status_code == 200

    response = client.get('/api/domains/other.custom.domain.com')

    assert response.json['ip'] == '2.2.2.2'
    assert response.json['domain'] == 'other.custom.domain.com'
    assert response.json['custom'] is True


def test_delete_non_existent_domain(client):
    response = client.delete('/api/custom-domains/invalid.domain.com')

    assert response.status_code == 404
    assert response.json == {}


def test_delete_domain(client, custom_domain):
    response = client.delete(f'/api/custom-domains/{custom_domain.domain}')

    assert response.status_code == 200
    assert response.json['domain'] == custom_domain.domain


def test_deleted_domain_does_not_show_up_in_get(client, custom_domain):
    client.delete(f'/api/custom-domains/{custom_domain.domain}')

    response = client.get(f'/api/domains/{custom_domain.domain}')

    assert response.status_code == 404


def test_get_all_custom_domains_initially_empty(client):
    response = client.get('/api/custom-domains')

    assert response.status_code == 200
    assert response.json['items'] == []


def test_get_all_custom_domains(client, custom_domain):
    response = client.get('/api/custom-domains')

    assert len(response.json['items']) == 1
    assert response.json['items'][0]['domain'] == custom_domain.domain


def test_get_multiple_custom_domains(client, custom_domain):
    client.post('/api/custom-domains',
                json={'domain': 'other.custom-domain-tp1.com',
                      'ip': '1.1.1.1'})
    response = client.get('/api/custom-domains')
    assert len(response.json['items']) == 2
    domains = [x['domain'] for x in response.json['items']]

    assert custom_domain.domain in domains
    assert 'other.custom-domain-tp1.com' in domains


def test_custom_domains_filter(client, custom_domain):
    response = client.get(f'/api/custom-domains?q={custom_domain.domain}')
    assert len(response.json['items']) == 1


def test_custom_domains_filter_all_filtered(client, custom_domain):
    response = client.get(f'/api/custom-domains?q=something_else')
    assert len(response.json['items']) == 0
