from fastapi import FastAPI, UploadFile, File
from fastapi.datastructures import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from aiworkout.find_angle import return_angle_squat, return_angle_bench, return_angle_deadlift
import cv2
import uvicorn
import numpy as np

from typing import Optional
from pydantic import BaseModel


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
