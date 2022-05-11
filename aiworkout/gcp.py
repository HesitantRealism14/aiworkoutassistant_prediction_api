import os
from google.cloud import storage
from termcolor import colored
from aiworkout.params import BUCKET_NAME, MODEL_NAME, MODEL_VERSION


def storage_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)
    local_model_name = 'pipeline3.pkl'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('pipeline3.pkl')
    print(colored(f"=> pipeline3.pkl uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove('pipeline3.pkl')

if __name__ == '__main__':
    storage_upload()
