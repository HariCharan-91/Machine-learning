import certifi
import time
import requests
from api_secrets import API_KEY_ASSEMBLYAI

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, CHUNK_SIZE=5242880):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    print(certifi.where())

    try:
        upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(filename))
        upload_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

    if 'upload_url' in upload_response.json():
        audio_url = upload_response.json()['upload_url']
        return audio_url
    else:
        return None

def transcribe(audio_url):
    try:
        transcript_response = requests.post(transcript_endpoint, json={'audio_url': audio_url}, headers=headers)
        transcript_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error during transcription: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting during transcription: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error during transcription: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred during transcription: {err}")

    if 'id' in transcript_response.json():
        job_id = transcript_response.json()['id']
        return job_id
    else:
        return None

def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result_url(audio_url):
    transcribe_id = transcribe(audio_url)
    while True:
        data = poll(transcribe_id)
        if 'status' in data and data['status'] == 'completed':
            return data, None
        elif 'status' in data and data['status'] == 'error':
            return data, data.get('error', 'Unknown error')

        print("waiting for 30 seconds")
        time.sleep(30)

textfile = ''
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)

    if data:
        text_filename = filename + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        print('Transcript saved')
    elif error:
        print("Error!!!", error)
