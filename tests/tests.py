# test_app.py
import pytest
from app import app  # Импортируем твое приложение из app.py

@pytest.fixture
def client():
    # Создаем тестовый клиент
    with app.test_client() as client:
        yield client

def test_get_notes_empty(client):
    """Проверяем, что GET /notes на пустом списке возвращает пустой список."""
    response = client.get('/notes')
    assert response.status_code == 200
    assert response.json == []

def test_create_note(client):
    """Проверяем создание заметки."""
    response = client.post('/notes', json={'title': 'Test', 'content': 'Content'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test'

# ... и так далее для остальных эндпоинтов (GET, PUT, DELETE)