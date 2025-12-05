import requests


class BaseTest:
    """Базовый класс для всех тестов API"""

    BASE_URL = "https://petstore.swagger.io/v2"
    TIMEOUT = 10

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data=None,
            params=None,
            expected_status: int = 200
    ) -> requests.Response:
        """Универсальный метод для выполнения HTTP-запросов"""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response

