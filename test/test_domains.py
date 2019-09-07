
def test_initially_one_student(client):
    # Le pega al endpoint!!!
    response = client.get('/api/domains/fi.uba.ar').json

    assert "ip" in response
    assert "domain" in response
    assert "custom" in response