from pydantic import BaseModel


class SPosition(BaseModel):
    id: int
    name: str
    is_leadership: bool

    class Config:
        orm_mode = True
