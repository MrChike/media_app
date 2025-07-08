from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from shared.config.base_settings import app_settings

REDIS_URL = (
    f"redis://:{app_settings.redis_password}@"
    f"{app_settings.redis_host}:{app_settings.redis_port}/0"
)

POSTGRES_URL = (
    f"postgresql+asyncpg://{app_settings.postgres_user}:"
    f"{app_settings.postgres_password}"
    f"@{app_settings.postgres_host}:"
    f"{app_settings.postgres_port}/"
    f"{app_settings.postgres_name}"
)

MONGODB_URL = (
  f"mongodb://{app_settings.mongodb_user}:{app_settings.mongodb_password}"
  f"@{app_settings.mongodb_host}:{app_settings.mongodb_port}/"
  f"{app_settings.mongodb_name}?authSource=admin"
)

# PostgreSQL
engine = create_async_engine(POSTGRES_URL, echo=False)
SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
Base = declarative_base()

# Redis
RedisClient = Redis.from_url(REDIS_URL, decode_responses=True)

# MongoDB
MongoClient = AsyncIOMotorClient(MONGODB_URL)
MongoDB = MongoClient[app_settings.mongodb_name]
