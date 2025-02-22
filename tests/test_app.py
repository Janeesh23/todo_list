import pytest
import sys
import os

# Ensure the app module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, Task

@pytest.fixture
def client():
    """Creates a test client with a temporary in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()  # Create tables for testing
        db.session.add(Task(title="Sample Task"))
        db.session.commit()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Cleanup

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'UP'}

def test_get_tasks(client):
    """Test retrieving all tasks."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 1

def test_create_task(client):
    """Test creating a new task."""
    response = client.post('/tasks', json={'title': 'New Task'})
    assert response.status_code == 201
    assert response.json['title'] == 'New Task'

def test_update_task(client):
    """Test updating an existing task."""
    response = client.put('/tasks/1', json={'completed': True})
    assert response.status_code == 200
    assert response.json['completed'] is True

def test_delete_task(client):
    """Test deleting a task."""
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert response.json == {'message': 'Task deleted'}
