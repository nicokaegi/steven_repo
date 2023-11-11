import time
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from flask import Flask
from typing import Union

from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)


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

def get_qr(active_time) -> Union[str, None]:
    
    feed_back_led_time = 5

    with Leds() as leds:
        leds.update(Leds.rgb_on(Color.YELLOW)) 
        leds.pattern = Pattern.blink(500)     
        cap = cv2.VideoCapture(0)
        for sec in range(active_time):
            ret, frame = cap.read()
            #print(frame.shape)
            time.sleep(1)
            qrcode = decoder(frame) 
            if qrcode:
                leds.update(Leds.rgb_on(Color.GREEN))
                print("success")
                time.sleep(feed_back_led_time)
                
                return qrcode
             
    leds.update(Leds.rgb_on(Color.RED))
    print("fail")
    time.sleep(feed_back_led_time)
    return None

app = Flask(__name__)

@app.route('/')
def main():
    qrcode = get_qr(60)
    if qrcode: 

        return qrcode
    
    else:
        return "failed to get qr code"

