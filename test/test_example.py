def test_example():
    assert 1 == 1


def test_initially_one_student(client):
    # Le pega al endpoint!!!
    response = client.get('/api/alumnos').json

    assert len(response) == 1
