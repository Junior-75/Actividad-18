import requests

class APIClient:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        # Inyección de dependencias: permitimos inyectar una sesión personalizada
        self.session = session or requests.Session()

    def get_todo(self, todo_id):
        response = self.session.get(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.json()

    def create_todo(self, data):
        response = self.session.post(f"{self.base_url}/todos", json=data)
        response.raise_for_status()
        return response.json()

    def update_todo(self, todo_id, data):
        response = self.session.put(f"{self.base_url}/todos/{todo_id}", json=data)
        response.raise_for_status()
        return response.json()

    def delete_todo(self, todo_id):
        response = self.session.delete(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.status_code == 200