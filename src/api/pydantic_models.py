from typing import List
from pydantic import BaseModel

class ParagraphClass(BaseModel):
  index: int
  paragraph: str

class BookType(BaseModel):
  name: str
  summary: List[ParagraphClass]

class AudioTitle(BaseModel):
  name: str

class AudiobookType(BaseModel):
  id:int
  name:str
  summary: List[ParagraphClass]