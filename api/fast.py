from fastapi import FastAPI, UploadFile, File
from fastapi.datastructures import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

from aiworkout.find_angle import return_angle_squat, return_angle_bench, return_angle_deadlift
from aiworkout.params import PATH_TO_GCP_MODEL, BUCKET_NAME

import cv2
import uvicorn
import pandas as pd
import numpy as np
import pickle
import base64
import json

import mediapipe as mp
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('credentials.json')

class Item(BaseModel):
    name: str
    description: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.post("/predict_pose")
async def make_predict(img:UploadFile=File(...)):
    client = storage.Client(credentials=credentials).bucket(BUCKET_NAME)
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imgRGB = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2RGB)
    with mp_pose.Pose() as pose_tracker:
        result = pose_tracker.process(image=imgRGB)
        pose_landmarks = result.pose_landmarks

    if pose_landmarks is not None:
        mp_drawing.draw_landmarks(
            image=imgRGB,
            landmark_list=pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS)
        pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]
        frame_height, frame_width = imgRGB.shape[:2]
        pose_landmarks *= np.array([frame_width, frame_height, frame_width])
        pose_landmarks = np.around(pose_landmarks, 5).flatten().tolist()

    x_pred = pd.DataFrame(pose_landmarks)
    x_pred = x_pred.T.to_numpy()

    blob = client.blob(PATH_TO_GCP_MODEL)
    blob.download_to_filename('model.pkl')
    with open('model.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file)
    y_pred = model.predict(x_pred[0].reshape(1,99))
    return {'workout pose':y_pred[0]}

@app.post("/getanglesquat")
async def getanglesquat(img: UploadFile=File(...)):
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return {'angle': return_angle_squat(cv2_img)}

@app.post("/getanglebench")
async def getanglebench(img: UploadFile=File(...)):
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return {'angle': return_angle_bench(cv2_img)}

@app.post("/getangledeadlift")
async def getanglebench(img: UploadFile=File(...)):
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return {'angle': return_angle_deadlift(cv2_img)}

@app.post("/annotate")
async def annotate(img:UploadFile=File(...)):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape
    with mp_holistic.Holistic(static_image_mode=True, model_complexity=2, enable_segmentation=True) as holistic:
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        out_image = image.copy()
        mp_drawing.draw_landmarks(
            out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
        mp_drawing.draw_landmarks(
            out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
        mp_drawing.draw_landmarks(
            out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
        mp_drawing.draw_landmarks(
            out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
    im = cv2.imencode('.jpg', out_image)[1]
    imdata = pickle.dumps(im)
    jstr = json.dumps({"annotated": base64.b64encode(imdata).decode('ascii')})
    return jstr

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
