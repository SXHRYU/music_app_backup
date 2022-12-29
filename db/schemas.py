from pydantic import BaseModel


class SongBase(BaseModel):
    id: int
    name: str


class SongCreate(SongBase):
    pass


class Song(SongBase):
    
    class Config:
        orm_mode = True
