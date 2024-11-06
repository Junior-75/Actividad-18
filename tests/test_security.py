from api_client import APIClient
from todo_service import TodoService
import pytest

def test_create_todo_injection_attempt(mocker):
    malicious_title = "'; DROP TABLE todos; --"
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 102,
        "title": malicious_title,
        "completed": False
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo(malicious_title)
    assert new_todo["title"] == malicious_title
    # Verificamos que la entrada se maneja adecuadamente
    mock_api_client.create_todo.assert_called_with({
        'title': malicious_title,
        'completed': False
    })
    
def test_create_todo_large_input(mocker):
    large_title = 'A' * 1000000  # Cadena de 1 millón de caracteres
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.side_effect = Exception("Payload too large")
    service = TodoService(mock_api_client)
    with pytest.raises(Exception) as exc_info:
        service.add_todo(large_title)
    assert "Payload too large" in str(exc_info.value)