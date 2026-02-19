from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from webapp.api.courses.routes import check_db_connection
from flask import Flask

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

@patch("webapp.api.courses.routes.check_db_connection")
def test_health(mock_db: MagicMock, client: FlaskClient) -> None:
    mock_db.return_value = True
    resp = client.get('/api/course/health')
    assert resp.status_code == 200

    assert resp.json == {
        "status": "ok",
        "database": "ok",
        "course_service": "ok"
    }

@patch("webapp.api.courses.routes.check_db_connection")
def test_health_if_not_connection(mock_db: MagicMock, client: FlaskClient) -> None:
    mock_db.return_value = False
    resp = client.get('/api/course/health')
    assert resp.status_code == 503

@patch("webapp.api.courses.routes.db.session.execute")
def test_check_db_connection(mock_db: MagicMock, app: Flask) -> None:
    mock_db.return_value = "Test"
    with app.app_context():
        res = check_db_connection()

    assert res == True

@patch("webapp.api.courses.routes.db.session.execute")
def test_check_db_connection_exception(mock_db: MagicMock, app: Flask) -> None:
    mock_db.side_effect = Exception()
    with app.app_context():
        res = check_db_connection()

    assert res == False

