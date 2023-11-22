from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic_models import *
from Database.Database import *
import audiobook_api
import sys
import uvicorn
import tts_api
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
    content.sort(key= lambda p : p[1])

  text = [paragraph[2] for paragraph in content]

  spk_id = tts_api.get_speaker()

  request_ids = []
  for paragraph in text:
    request_ids.append(tts_api.request_conversion(spk_id, paragraph))

  audios = []
  for id in request_ids:
    audios.append(tts_api.fetch_conversion(id))

  for i in range(len(audios)):
    set_paragraph_status(content[i], audios[i])

  audio_file = audiobook_api.build_audio(audios, filename)
  headers = {'Content-Disposition': f'attachment; filename="{filename}"'}

  return FileResponse(audio_file,  headers=headers, media_type="audio/wav")

@app.post("/api/generate/{id}", tags=["Audio"], status_code=200)
async def merge(id: int):
  content, filename = retrieve_content(id)
  if type(content) == str:
    raise HTTPException(status_code=404, detail=content)
  else:
    content.sort()

  audio_file = audiobook_api.build_audio(filename)
  headers = {'Content-Disposition': f'attachment; filename="{filename}"'}

  return FileResponse(audio_file,  headers=headers, media_type="audio/wav")