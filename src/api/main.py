from fastapi import Depends, FastAPI, HTTPException
from pydantic_models import *
from Database.Database import *
import uvicorn
app = FastAPI()

@app.post("/api/create", tags=["Create"], status_code=200)
async def create(bookData: BookType):
  response = create_audio(bookData.name, bookData.summary)
  return response

@app.get("/api/select_by_name", tags=["Query"], status_code=200)
async def select(title: AudioTitle = Depends()):
  query = check_audio(title.name)
  print(query)
  if type(query) == int:
    response = {"audio_id": query}
  else:
    raise HTTPException(status_code=404, detail=query)
  return response

@app.put("/api/update/{book_id}", tags=["Query"], status_code=200)
async def update(bookData: BookType, book_id: int):
  query = update_audio(book_id, bookData.name, bookData.summary)

  if type(query) == int:
    response = {"detail": "Audio modified succesfully."}
  else:
    raise HTTPException(status_code=404, detail=query)
  return response