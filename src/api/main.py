from fastapi import FastAPI
from pydantic_models import *
from Database.Database import *
import uvicorn
app = FastAPI()

@app.post("/api/create")
async def create(bookData: BookType):
  response = create_audio(bookData.name, bookData.summary)
  return response
