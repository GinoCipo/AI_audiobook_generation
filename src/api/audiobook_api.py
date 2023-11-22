import re
from Database.Database import *
from pydub import AudioSegment
from urllib.request import urlretrieve
import os, shutil

def extract_number(filename):
    match = re.search(r'part(\d+)\.wav', filename)
    if match:
        return int(match.group(1))
    return -1  # Return -1 if pattern not found or for non-matching files

def build_paragraphs(urls, paper_name):
    buffer = []
    filepaths = []
    for part, url in enumerate(urls):
        buffer.append(urlretrieve(url, f"part{part}.wav")[0])
        filepaths.append(f"part{part}.wav")

    destination_path = f"output/{paper_name}"
    os.mkdir(destination_path)
    for filepath in filepaths:
        shutil.move(filepath, destination_path)
    

def build_audio(paper_name):
    buffer = [f"output/{paper_name}/" + part for part in os.listdir(f"output/{paper_name}")]
    buffer.sort(key=extract_number)
    audios = [AudioSegment.from_wav(wav_file) for wav_file in buffer]
    combined = AudioSegment.empty()
    for audio in audios:
        combined += audio
    filepath = f"{paper_name}.wav"
    combined.export(filepath, format="wav")

    for filename in buffer:
        #file_path = os.path.join("api/buffer", filename)
        try:
            if os.path.isfile(filename) or os.path.islink(filename):
                os.unlink(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (filename, e))

    destination_path = f"output/{paper_name}/{filepath}"
    shutil.move(filepath, destination_path)

    return destination_path

if __name__ == "__main__":
    print("This module is used to download and concatenate a list of audios under a paper_name.")