from fastapi import FastAPI, UploadFile, File
from fastapi.datastructures import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from aiworkout.find_angle import return_angle_squat, return_angle_bench, return_angle_deadlift
import cv2
import uvicorn
import numpy as np
import joblib

from typing import Optional
from pydantic import BaseModel

PATH_TO_LOCAL_MODEL = 'raw_data/train_img'

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

@app.get("/predict_pose")
def make_predict(img):

    model = joblib.load(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(img)

    classes = {'bench':0,
               'deadlift':1,
               'squat':2}
    return {'workout_pose':classes.get(np.argmax(y_pred),'workout pose not found')}

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




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
