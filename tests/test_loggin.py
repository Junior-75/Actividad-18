import logging
from api_client import APIClient

def test_logging(caplog, mocker):
    caplog.set_level(logging.INFO)
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Todo",
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    client.get_todo(1)

    assert "Obteniendo todo con ID 1" in caplog.text
    assert "Todo obtenido: {'id': 1, 'title': 'Test Todo', 'completed': False}" in caplog.text