import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Настройка окружения перед тестами"""
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
    except Exception as e:
        error_msg = f"⚠️  API не доступен: {e}"
        print(error_msg)
        pytest.skip("API не доступен")

    yield

    print("\n" + "=" * 50)
    print("ЗАВЕРШЕНИЕ ТЕСТОВ")
    print("=" * 50)