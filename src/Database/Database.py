from pony.orm import *
import sys

db = Database()
db.bind(provider="sqlite", filename="db.AIaudiobooks", create_db=True)

class Paragraph(db.Entity):
  id= PrimaryKey(int, auto=True)
  index= Required(int)
  body= Required(str)
  status= Required(str)
  audio= Optional(str)
  owner= Required("Audiobook", reverse="summary")

class Audiobook(db.Entity):
  id= PrimaryKey(int, auto=True)
  name= Required(str)
  summary= Set("Paragraph", reverse="owner")

db.generate_mapping(create_tables=True)

@db_session
def create_audio(
  name,
  summary 
):
  new_audio = Audiobook(
    name=name
  )
  sum = []
  for text in summary:
    if not text.paragraph:
      continue
    new_paragraph = Paragraph(
      index = text.index,
      body = text.paragraph,
      status = "pending",
      audio = "",
      owner = new_audio
    )
    sum.append(({
      "index": new_paragraph.index,
      "body": new_paragraph.body,
      "status": new_paragraph.status,
      "audio": new_paragraph.audio,
      "owner": new_paragraph.owner.name
    }))

  new_audio.flush()
  data = {
    "id": new_audio.id,
    "name": new_audio.name,
    "summary": sum
  }

  return data

@db_session
def check_audio(
  name
):
  try:
    target_audio = Audiobook.select(lambda a: a.name == name)[:]
    print(target_audio)
    return target_audio[0].id
  except:
    return "Audiobook title does not exist."

@db_session
def update_audio(
  id,
  name,
  summary
):
  try:
    target_audio = Audiobook[id]
  except:
    return "Audio id does not exist."

  target_audio.name = name

  for paragraph in summary:
    target_paragraph = target_audio.summary.select(lambda p: p.index == paragraph.index)[:][0]
    target_paragraph.body = paragraph.paragraph

  return 200

@db_session
def retrieve_content(
  id
):
  try:
    target_audio = Audiobook[id]
  except:
    return "Audio id does not exist."
  
  body = []
  for paragraph in target_audio.summary:
    body.append((paragraph.id, paragraph.index, paragraph.body))

  return body, Audiobook[id].name

@db_session
def set_paragraph_status(
  id, 
  url
):
  try:
    target_paragraph = Paragraph[id]
  except:
    return "Paragraph does not exist."

  target_paragraph.status = "done"
  target_paragraph.audio = url

  return 1

@db_session
def update_paragraph_body(
  id,
  index,
  text
):
  try:
    query = Audiobook[id].summary.select(lambda p: p.index == index)[:]
    target_paragraph = query[0]
  except:
    return "Paragraph does not exist."

  target_paragraph.body = text
  return target_paragraph.id