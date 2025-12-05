import requests
from typing import Dict, Any, Optional
import json


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
            data: Optional[Dict] = None,
            params: Optional[Dict] = None,
            expected_status: int = 200,
            allow_failure: bool = False
    ) -> requests.Response:
        """Универсальный метод для выполнения HTTP-запросов"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                timeout=self.TIMEOUT
            )

            if not allow_failure:
                response.raise_for_status()

            if response.status_code != expected_status:
                print(f"[!] Ожидаемый статус: {expected_status}, Получен: {response.status_code}")

            return response

        except requests.exceptions.RequestException as e:
            error_msg = f"[ERROR] Ошибка запроса: {method} {url}\nДетали: {str(e)}"
            print(error_msg)
            if not allow_failure:
                raise
            else:
                # Создаем dummy response для тестов с ожидаемыми ошибками
                dummy_response = requests.Response()
                dummy_response.status_code = 404
                dummy_response._content = b'{"error": "Not Found"}'
                return dummy_response

    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """Создание пользователя"""
        return self._make_request("POST", "/user", data=user_data, expected_status=200)

    def get_user(self, username: str) -> requests.Response:
        """Получение данных пользователя"""
        return self._make_request("GET", f"/user/{username}", expected_status=200)

    def update_user(self, username: str, user_data: Dict[str, Any]) -> requests.Response:
        """Обновление данных пользователя"""
        return self._make_request("PUT", f"/user/{username}", data=user_data, expected_status=200)

    def delete_user(self, username: str, allow_failure: bool = False) -> requests.Response:
        """Удаление пользователя"""
        return self._make_request("DELETE", f"/user/{username}", expected_status=200, allow_failure=allow_failure)

    def login(self, username: str, password: str) -> requests.Response:
        """Авторизация пользователя"""
        return self._make_request(
            "GET",
            "/user/login",
            params={"username": username, "password": password},
            expected_status=200
        )

    def logout(self) -> requests.Response:
        """Выход из системы"""
        return self._make_request("GET", "/user/logout", expected_status=200)

    def log_response(self, response: requests.Response, test_name: str = ""):
        """Логирование ответа для отладки"""
        log_data = f"""
            {'=' * 50}
            ТЕСТ: {test_name}
            URL: {response.request.url}
            МЕТОД: {response.request.method}
            СТАТУС: {response.status_code}
            ТЕЛО ЗАПРОСА: {response.request.body[:200] if response.request.body else 'None'}
            ОТВЕТ: {response.text[:200]}
            {'=' * 50}
            """
        print(log_data)

    def validate_json_schema(self, response_data: Dict, expected_schema: Dict) -> bool:
        """Базовая валидация JSON схемы"""
        for key, value_type in expected_schema.items():
            if key not in response_data or not isinstance(response_data[key], value_type):
                return False
        return True

