from Database.Database import *
import requests
import json
import time

URL = "https://api.genny.lovo.ai"
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "a924998b-fa48-4046-ae06-2f387c79b773"
    }

def get_speaker():
    speakers = requests.get(URL + "/api/v1/speakers", headers=headers).json()
    print(f'Fetched a total of # {speakers["totalCount"]} speakers!')

    speaker_found = next(filter(lambda speaker: speaker['displayName'] == 'Diego Gallardo', speakers['data']), None)
    speaker_id = speaker_found["id"]
    print(f'The speaker ID we will use is {speaker_id}')
    return(speaker_id)

def request_conversion(speaker_id, text):
    tts_body = {
        "speaker": speaker_id,
        "text": text
    }

    tts_job = requests.post(URL + "/api/v1/tts", headers=headers, data=json.dumps(tts_body)).json()
    job_id = tts_job['id']
    print(f'TTS Job is created with ID: {job_id}')
    return job_id

def fetch_conversion(job_id):
    job_complete = False
    tts_url = ''
    retry_count = 0

    while not job_complete:
        job_res = requests.get(URL + f'/api/v1/tts/{job_id}', headers=headers).json()
        status = job_res['status']
        if (status != 'done'):
            time.sleep(1)
            retry_count += 1
        else:
            job_complete = True
            tts_url = job_res['data'][0]['urls'][0]

    print(f'TTS file is available at: {tts_url}')
    return tts_url

if __name__ == "__main__":
    print("This Python module is used to import all of the functions used to turn a text into audio.")