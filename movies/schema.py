from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Union


class MovieSchema(BaseModel):
    title: str
    actors: Optional[str] = None
    year: Optional[int] = None


class MovieResponseSchema(MovieSchema):
    id: Union[int, str] = Field(alias="_id")  # Handles PostgreSQL and Mongo
    model_config = ConfigDict(
        from_attributes=True,  # Allows ORM instances (SQLAlchemy)
        populate_by_name=True  # Allows alias resolution (_id → id)
    )
