from pydantic import BaseModel, ConfigDict
from typing import Optional

class MovieSchema(BaseModel):
    title: str
    actors: Optional[str] = None
    year: Optional[int] = None


class MovieResponseSchema(MovieSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)    