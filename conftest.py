import pytest
import requests
import allure


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Настройка окружения перед тестами"""
    with allure.step("Проверка доступности API"):
        print("\n" + "=" * 50)
        print("НАСТРОЙКА ОКРУЖЕНИЯ")
        print("=" * 50)

    try:
        response = requests.get(
            "https://petstore.swagger.io/v2/user/login",
            params={"username": "test", "password": "test"},
            timeout=5
        )
        print(f"✅ API доступен (статус: {response.status_code})")
        allure.attach(
            f"API доступен: {response.status_code}",
            name="Инициализация",
            attachment_type=allure.attachment_type.TEXT
        )
    except Exception as e:
        error_msg = f"⚠️  API не доступен: {e}"
        print(error_msg)
        allure.attach(error_msg, name="Ошибка инициализации", attachment_type=allure.attachment_type.TEXT)
        pytest.skip("API не доступен")

    yield

    with allure.step("Завершение тестов"):
        print("\n" + "=" * 50)
        print("ЗАВЕРШЕНИЕ ТЕСТОВ")
        print("=" * 50)