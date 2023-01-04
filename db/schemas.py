from pydantic import BaseModel


class SongBase(BaseModel):
    id: int
    name: str
    path: str

class SongCreate(SongBase):
    data: bytes

class Song(SongBase):
    
    class Config:
        orm_mode = True
