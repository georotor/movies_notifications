from core.config import Settings


class TestSettings(Settings):
    service_url: str = 'http://127.0.0.1:8000'


test_settings = TestSettings()
