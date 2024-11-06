from loguru import logger
from pydantic import DirectoryPath, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env", env_file_encodings="utf-8"
    )

    use_selenium: bool
    url_base_name: str
    url_pages: int
    use_list: bool
    url_list_file: FilePath
    save_dir: DirectoryPath
    container_str: str
    class_str: str
    log_level: str


settings = Settings()

logger.remove()
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="2 days",
    compression="zip",
    level=settings.log_level,
)
