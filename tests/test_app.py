import pytest
from flask import Flask
from app import app, db, Todo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_add(client):
    rv = client.post('/add', data=dict(title="Test task"), follow_redirects=True)
    assert rv.status_code == 200
    with app.app_context():
        assert Todo.query.count() == 1

def test_finish_task(client):
    rv = client.post('/add', data=dict(title="Test task"), follow_redirects=True)
    rv = client.get('/complete/1', follow_redirects=True)
    assert rv.status_code == 200
    with app.app_context():
        assert Todo.query.get(1).complete == True

def test_delete(client):
    rv = client.post('/add', data=dict(title="Test task"), follow_redirects=True)
    rv = client.get('/delete/1', follow_redirects=True)
    assert rv.status_code == 200
    with app.app_context():
        assert Todo.query.count() == 0