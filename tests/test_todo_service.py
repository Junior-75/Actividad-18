from hypothesis import given, strategies as st
from todo_service import TodoService
from api_client import APIClient
from unittest.mock import patch

# Mock: Simulamos el comportamiento del APIClient
def test_get_todo_details(mocker):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.get_todo.return_value = {
        "id": 1,
        "title": "test todo",
        "completed": False
    }
    service = TodoService(mock_api_client)
    todo = service.get_todo_details(1)
    assert todo["title"] == "Test Todo"
    mock_api_client.get_todo.assert_called_once_with(1)

# Stub: Usamos un objeto simple con respuestas predefinidas
class FakeAPIClient:
    def get_todo(self, todo_id):
        return {
            "id": todo_id,
            "title": "fake todo",
            "completed": False
        }

def test_get_todo_details_with_fake_client():
    fake_client = FakeAPIClient()
    service = TodoService(fake_client)
    todo = service.get_todo_details(1)
    assert todo["title"] == "Fake Todo"

# Prueba de integración con la API real
def test_complete_todo_integration():
    api_client = APIClient("https://jsonplaceholder.typicode.com")
    service = TodoService(api_client)
    todo = service.complete_todo(1)
    assert todo["completed"] == True

# Spy: Verificamos que se llamaron métodos internos
def test_add_todo_calls_create_todo(mocker):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 101,
        "title": "New Todo",
        "completed": False
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo("New Todo")
    assert new_todo["id"] == 101
    mock_api_client.create_todo.assert_called_once()

@given(title=st.text(min_size=1), completed=st.booleans())
def test_add_todo_with_hypothesis(mocker, title, completed):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 101,
        "title": title,
        "completed": completed
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo(title, completed)
    assert new_todo["title"] == title
    assert new_todo["completed"] == completed

def test_get_todo_details_with_fixture(mocker, todo_service):
    mock_get_todo = mocker.patch.object(APIClient, 'get_todo', return_value={
        "id": 1,
        "title": "test todo",
        "completed": False
    })
    todo = todo_service.get_todo_details(1)
    assert todo["title"] == "Test Todo"
    mock_get_todo.assert_called_once_with(1)

