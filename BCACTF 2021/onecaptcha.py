#!/usr/bin/python3
import requests
import json
import os
import base64
from PIL import Image

#receive image and store
def clearImages():
    os.system("rm -rf images/")
    os.system("mkdir images")

def base64decode(dat):
    return base64.b64decode(dat)

r = requests.post("http://misc.bcactf.com:49158/api/challenge")
data = r.json()
token = data['challenge']

while True:
    data = r.json()
    if "flag" in json.dumps(data):
        print(data['flag'])
        break
    clearImages()
    try:
        print(f"Level {data['stage']} of {data['stages']}")
        print(f"Time limit: {data['time']}")
    except:
        print(data['error'])
        break
    token = data['challenge']

    f = open("images/captcha.png", "wb+")
    f.write(base64decode(data['expected'].split(",")[-1]))
    f.close()

    for index,value in enumerate(data['images']):
        f = open(f"images/challenge{index}.png", 'wb+')
        f.write(base64decode(value.split(",")[-1]))
        f.close()

    response = []

    im = Image.open("images/captcha.png")
    p = im.getcolors()
    p.sort()
    targetPixels = p[-1][0]
    targetPixels2 = p[-2][0]

    for x in range(9):
        im = Image.open(f"images/challenge{x}.png")
        p = im.getcolors()
        p.sort()
        response.append((p[-1][0] == targetPixels) or (p[-2][0] == targetPixels2))

    r = requests.post("http://misc.bcactf.com:49158/api/challenge", headers={"X-Captcha-Challenge": token}, json={"answer": response})
