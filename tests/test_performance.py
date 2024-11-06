from api_client import APIClient

def test_get_todo_performance(benchmark, mocker):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Todo",
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)

    def fetch_todo():
        client.get_todo(1)

    result = benchmark(fetch_todo)
    assert result is None  # La función no retorna nada