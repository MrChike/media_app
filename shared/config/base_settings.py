from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    omdb_movies_api_key: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_name: str
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str
    mongodb_port: int
    mongodb_name: str
    redis_password: str
    redis_host: str
    redis_port: str


app_settings = AppSettings()  # type: ignore
