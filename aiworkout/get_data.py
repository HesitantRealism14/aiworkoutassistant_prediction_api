import numpy as np
from google.cloud import storage
from aiworkout.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH
import tqdm
from PIL import Image

def get_data_from_gcp(**kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}"
    classes = {'bench':0,
               'deadlift':1,
               'squat':2}
    imgs= []
    labels = []

    for cl,i in classes.items():
        img_path = [elt for elt in f"{BUCKET_TRAIN_DATA_PATH}/{cl}" if elt.find('.jpg')>0]

        for img in tqdm(img_path):
            path = f"{BUCKET_TRAIN_DATA_PATH}/{cl}/{img}"
            image = Image.open(path).convert('RGB')
            image = image.resize((256,256))
            imgs.append(np.array(image))
            labels.append(i)

    X = np.array(imgs)
    y = np.array(labels)

    return X,y

if __name__ == '__main__':
    img_data = get_data_from_gcp()
