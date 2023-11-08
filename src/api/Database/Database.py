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
    for paragraph in summary:
        new_paragraph = Paragraph(
            index = paragraph.index,
            body = paragraph.paragraph,
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

    data = {
        "id": new_audio.id,
        "name": new_audio.name,
        "summary": sum
    }

    return data
