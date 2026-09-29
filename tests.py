import pytest
from app import app, notes  # импортируем и приложение, и список заметок


@pytest.fixture
def client():
    """Тестовый клиент Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_state():
    """
    Автоматически очищает глобальное состояние перед каждым тестом.
    Без этого данные из одного теста попадут в следующий.
    """
    notes.clear()
    # сбрасываем next_id через модуль app
    import app as app_module
    app_module.next_id = 1
    yield
    notes.clear()
    app_module.next_id = 1


# ---------- GET /notes ----------

def test_get_notes_empty(client):
    """Пустой список заметок."""
    response = client.get('/notes')
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_notes_with_data(client):
    """Список из нескольких заметок."""
    client.post('/notes', json={'title': 'A', 'content': 'aaa'})
    client.post('/notes', json={'title': 'B', 'content': 'bbb'})

    response = client.get('/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['title'] == 'A'
    assert data[1]['title'] == 'B'


# ---------- GET /notes/<id> ----------

def test_get_note_by_id(client):
    """Получение существующей заметки."""
    created = client.post('/notes', json={'title': 'Test', 'content': 'Body'}).get_json()

    response = client.get(f"/notes/{created['id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test'
    assert data['content'] == 'Body'
    assert data['id'] == created['id']


def test_get_note_not_found(client):
    """Заметка с несуществующим id — 404."""
    response = client.get('/notes/999')
    assert response.status_code == 404


# ---------- POST /notes ----------

def test_create_note_success(client):
    """Успешное создание заметки."""
    response = client.post('/notes', json={'title': 'New', 'content': 'Text'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['title'] == 'New'
    assert data['content'] == 'Text'


def test_create_note_increments_id(client):
    """id увеличивается с каждой новой заметкой."""
    r1 = client.post('/notes', json={'title': 'A', 'content': 'a'}).get_json()
    r2 = client.post('/notes', json={'title': 'B', 'content': 'b'}).get_json()
    assert r1['id'] == 1
    assert r2['id'] == 2


def test_create_note_without_json(client):
    """Запрос без Content-Type: application/json — 400."""
    response = client.post('/notes', data='not json')
    assert response.status_code == 400


def test_create_note_missing_fields(client):
    """Не хватает обязательного поля — 400."""
    response = client.post('/notes', json={'title': 'Only title'})
    assert response.status_code == 400


def test_create_note_missing_content(client):
    """Не хватает content — 400."""
    response = client.post('/notes', json={'content': 'Only content'})
    assert response.status_code == 400


# ---------- PUT /notes/<id> ----------

def test_update_note_full(client):
    """Полное обновление заметки."""
    created = client.post('/notes', json={'title': 'Old', 'content': 'Old body'}).get_json()

    response = client.put(
        f"/notes/{created['id']}",
        json={'title': 'New', 'content': 'New body'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'New'
    assert data['content'] == 'New body'


def test_update_note_partial(client):
    """Обновление только title — content остаётся прежним."""
    created = client.post('/notes', json={'title': 'Old', 'content': 'Body'}).get_json()

    response = client.put(f"/notes/{created['id']}", json={'title': 'New'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'New'
    assert data['content'] == 'Body'  # не изменилось


def test_update_note_not_found(client):
    """Обновление несуществующей заметки — 404."""
    response = client.put('/notes/999', json={'title': 'X', 'content': 'Y'})
    assert response.status_code == 404


def test_update_note_without_json(client):
    """PUT без JSON — 400."""
    created = client.post('/notes', json={'title': 'A', 'content': 'a'}).get_json()
    response = client.put(f"/notes/{created['id']}", data='plain text')
    assert response.status_code == 400


# ---------- DELETE /notes/<id> ----------

def test_delete_note_success(client):
    """Успешное удаление заметки."""
    created = client.post('/notes', json={'title': 'To delete', 'content': 'X'}).get_json()

    response = client.delete(f"/notes/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Note deleted'

    # проверяем, что заметки больше нет
    check = client.get(f"/notes/{created['id']}")
    assert check.status_code == 404


def test_delete_note_not_found(client):
    """Удаление несуществующей заметки — 404."""
    response = client.delete('/notes/999')
    assert response.status_code == 404


def test_delete_reduces_list(client):
    """После удаления список становится короче."""
    client.post('/notes', json={'title': 'A', 'content': 'a'})
    second = client.post('/notes', json={'title': 'B', 'content': 'b'}).get_json()

    client.delete(f"/notes/{second['id']}")

    response = client.get('/notes')
    assert len(response.get_json()) == 1