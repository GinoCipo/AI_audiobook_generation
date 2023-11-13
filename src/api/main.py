from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic_models import *
from Database.Database import *
import audiobook_api
import sys
import uvicorn
sys.path.append("..")
import tts
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

@app.post("/api/generate/{id}", tags=["Audio"], status_code=200)
async def generate(id: int):
  content, filename = retrieve_content(id)
  if type(content) == str:
    raise HTTPException(status_code=404, detail=content)
  else:
    content.sort()
  
  text = [paragraph[1] for paragraph in content]

  spk_id = tts.get_speaker()

  request_ids = []
  for paragraph in text:
    request_ids.append(tts.request_conversion(spk_id, paragraph))

  audios = []
  for id in request_ids:
    audios.append(tts.fetch_conversion(id))

  audio_file = audiobook_api.build_audio(audios, filename)

  return FileResponse(audio_file)