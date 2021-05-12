from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import cv2
from fastapi.responses import HTMLResponse, StreamingResponse
from fer import FER
import matplotlib.pyplot as plt
import aiofiles
app = FastAPI()

# app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get('/')  # basic get view
def basic_view():
    return {"WELCOME": "GO TO /docs route "}


@app.get('/predict', response_class=HTMLResponse)  # data input by forms
async def main():
    content = """
    <body>
    <form action = "/predict" method="post">
    <p> Upload an image of your face</p> 
    <input type="file">
    <input type="submit" value="Submit">
    </form>
    </body>"""
    return HTMLResponse(content= content)


@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    img = plt.imread(file.filename)
    detector = FER(mtcnn=True)
    emo = detector.detect_emotions(img)[0]['emotions']
    return {"Emotions Detected": emo}
