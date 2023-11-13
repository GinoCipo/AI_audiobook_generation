from pydub import AudioSegment
from urllib.request import urlretrieve
import os, shutil

def build_audio(urls, paper_name):
    buffer = []
    for part, url in enumerate(urls):
        path = os.path.join("api/buffer", f"{part}.wav")
        buffer.append(urlretrieve(url, path)[0])
    
    audios = [AudioSegment.from_wav(wav_file) for wav_file in buffer]
    combined = AudioSegment.empty()
    for audio in audios:
        combined += audio
    filepath = f"api/output/{paper_name}.wav"
    combined.export(filepath, format="wav")

    for filename in os.listdir("api/buffer"):
        file_path = os.path.join("api/buffer", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return filepath

if __name__ == "__main__":
    print("This module is used to download and concatenate a list of audios under a paper_name.")