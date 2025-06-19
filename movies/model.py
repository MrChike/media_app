# === POSTGRESQL MODEL ===

from sqlalchemy import Column, Integer, String
from shared.db.connection import Base
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    actors = Column(String)
    year = Column(Integer)


# === MONGODB MODEL ===

from beanie import Document

class MovieMongo(Document):
    title: str
    actors: str
    year: int

    class Settings:
        name = "movies"  # Collection name