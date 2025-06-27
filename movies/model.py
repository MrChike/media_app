from sqlalchemy import Column, Integer, String
from shared.db.connection import Base
from beanie import Document


# === POSTGRESQL MODEL ===

class PostgresMovie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    actors = Column(String)
    year = Column(Integer)


# === MONGODB MODEL ===

class MongoMovie(Document):
    title: str
    actors: str
    year: int

    class Settings:
        name = "movies"  # Collection name
