from io import StringIO
import re
import zipfile
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
    try:
        os.mkdir(destination_path)
    except:
        print("This directory already exists.")

    for filepath in filepaths:
        shutil.move(filepath, destination_path)
    zip_filename = f"output/{paper_name}/{paper_name}.zip"

    filepaths = [destination_path + "/" + file for file in filepaths]
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in filepaths:
            zipf.write(file, os.path.basename(file))
    
    return zip_filename

def build_paragraph(url, index, book):
    filename = f"part{index}.wav"
    buffer = urlretrieve(url, filename)[0]
    destination_path = f"output/{book}"
    try:
        os.mkdir(destination_path)
    except:
        print("This directory already exists.")

    try:
        if os.path.isfile(destination_path + "/" + filename) or os.path.islink(destination_path + "/" + filename):
            os.unlink(destination_path + "/" + filename)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (e))

    shutil.move(filename, destination_path)

    return destination_path + "/" + filename

def build_audio(paper_name):
    zip_path = f"output/{paper_name}/{paper_name}.zip"
    try:
        if os.path.isfile(zip_path) or os.path.islink(zip_path):
            os.unlink(zip_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (e))

    buffer = [f"output/{paper_name}/" + part for part in os.listdir(f"output/{paper_name}")]
    buffer.sort(key=extract_number)
    audios = [AudioSegment.from_wav(wav_file) for wav_file in buffer]
    combined = AudioSegment.empty()
    for audio in audios:
        combined += audio
    filepath = f"{paper_name}.wav"
    combined.export(filepath, format="wav")

    #for filename in buffer:
    #    try:
    #        if os.path.isfile(filename) or os.path.islink(filename):
    #            os.unlink(filename)
    #        elif os.path.isdir(filename):
    #            shutil.rmtree(filename)
    #    except Exception as e:
    #        print('Failed to delete %s. Reason: %s' % (filename, e))

    destination_path = f"output/{paper_name}/{filepath}"
    shutil.move(filepath, destination_path)

    return destination_path

if __name__ == "__main__":
    print("This module is used to download and concatenate a list of audios under a paper_name.")