from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import cv2
from fastapi.responses import HTMLResponse, StreamingResponse
from fer import FER
import matplotlib.pyplot as plt
import aiofiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)  # basic get view
async def getRoot():
    async with aiofiles.open("templates\index.html", mode="r") as f:
        data = await f.read()
    return data

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    img = plt.imread(file.filename)
    detector = FER(mtcnn=True)
    emo = detector.detect_emotions(img)[0]['emotions']
    return {"Emotions Detected": emo}
