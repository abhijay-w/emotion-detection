from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import shutil
import os
from fastapi.responses import HTMLResponse
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


@app.get('/detect', response_class=HTMLResponse)
async def proceed():
    async with aiofiles.open("templates\emotions.html", mode="r") as f:
        data = await f.read()
    return data


@app.post("/upload")
def emotiondetection(image: UploadFile = File(...)):
    save_file(image, path="temp", save_as="temp")
    return{"text": "File Uploaded Successfully"}


@app.post("/predict")
def emotions():
    img = plt.imread("temp/temp.jpg")
    detector = FER(mtcnn=True)
    key_value = detector.detect_emotions(img)[0]['emotions']
    emo = {}
    sorted_keys = sorted(key_value, key=key_value.get, reverse=True)
    for w in sorted_keys:
        emo[w] = key_value[w]
    emotions = list(emo.keys())[0:3]
    return {"emo": emotions}


def save_file(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file
