import os
import pathlib


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    __db_path = os.path.join(BASE_DIR, 'database.db')
    # Database coupling
    DATABASE_URL: str = os.environ.get("DATABASE_URL", f"sqlite+aiosqlite:///{__db_path}")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()