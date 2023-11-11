import time
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from flask import Flask
from typing import Union
import asyncio
import datetime


def decoder(image) -> Union[str, None]:
    
    gray_img = cv2.cvtColor(image,0)
    qrcode = decode(gray_img)
    
    if len(qrcode) != 0:
        obj = qrcode[0]
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))

        qrcodeData = obj.data.decode("utf-8")
        qrcodeType = obj.type
    
        return str(qrcodeData)
    
    return None

async def get_qr() -> Union[str, None]:

    endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
    cap = cv2.VideoCapture(0)
    while datetime.datetime.now() <= endTime :
        ret, frame = cap.read()
        qrcode = decoder(frame)
        if qrcode:
            return qrcode
             
    return None

app = Flask(__name__)

@app.route('/')
async def main():

    print("active")

    try:

        async with asyncio.timeout(60):
            qrcode=await get_qr()
            print("success : ", qrcode)
    except TimeoutError:
           qrcode = None 
           print("failed to get qr")
    
    if qrcode: 

        return qrcode
    
    else:
        return "failed to get qr code"

