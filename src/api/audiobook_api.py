from pydub import AudioSegment
from urllib.request import urlretrieve
import os, shutil

def build_audio(urls, paper_name):
    buffer = []
    filepaths = []
    for part, url in enumerate(urls):
        #path = "api/buffer" + "/" + f"{part}.wav"
        #open(path, "w+")
        buffer.append(urlretrieve(url, f"part{part}.wav")[0])
        filepaths.append(f"part{part}.wav")

    audios = [AudioSegment.from_wav(wav_file) for wav_file in buffer]
    combined = AudioSegment.empty()
    for audio in audios:
        combined += audio
    filepath = f"{paper_name}.wav"
    combined.export(filepath, format="wav")

    for filename in filepaths:
        #file_path = os.path.join("api/buffer", filename)
        try:
            if os.path.isfile(filename) or os.path.islink(filename):
                os.unlink(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (filename, e))

    destination_path = f"output/{filepath}"
    shutil.move(filepath, destination_path)

    return destination_path

if __name__ == "__main__":
    print("This module is used to download and concatenate a list of audios under a paper_name.")