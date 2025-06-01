from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class AppSettings(BaseSettings):
    omdb_movies_api_key: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    redis_password: str
    redis_host: str
    redis_port: int


app_settings = AppSettings() # type: ignore
