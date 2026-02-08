from flask.testing import FlaskClient


def test_create_order(client: FlaskClient) -> None:
    resp = client.post('/api/course/', json={
        'name': 'Test',
        'description': 'test',
        'start_date': '2026-10-10',
        'end_date': '2026-10-10',
        'price': 100
    })
    assert resp.status_code == 201

def test_get_by_id(client: FlaskClient) -> None:
    _ = client.post('/api/course/', json={
        'name': 'Test',
        'description': 'test',
        'start_date': '2026-10-10',
        'end_date': '2026-10-10',
        'price': 100
    })

    resp2 = client.get('/api/course/1', json={"course_id": 1})
    assert resp2.status_code == 200

def test_get_by_name(client: FlaskClient) -> None:
    _ = client.post('/api/course/', json={
        'name': 'Test',
        'description': 'test',
        'start_date': '2026-10-10',
        'end_date': '2026-10-10',
        'price': 100
    })

    resp = client.get('/api/course/?name=Test', json={'name': 'Test'})
    assert resp.status_code == 200

def test_update_course_and_delete(client: FlaskClient) -> None:
    _ = client.post('/api/course/', json={
        'name': 'Test',
        'description': 'test',
        'start_date': '2026-10-10',
        'end_date': '2026-10-10',
        'price': 100
    })
    resp = client.patch('/api/course/1', json={
        'name': 'Test',
        'description': 'update test',
        'start_date': '2026-10-10',
        'end_date': '2026-10-10',
        'price': 100
    })
    assert resp.status_code == 200

    resp = client.delete('/api/course/1', json={
        'course_id': 1
    })

    assert resp.status_code == 204
