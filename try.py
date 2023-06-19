import boto3
from PIL import Image, ImageDraw, ImageFont
import io
import cv2
import json
from PIL import Image
import requests


import cv2

def capture_frame(url):
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()  # 讀取一張影格

    if ret:
        cv2.imwrite("captured_frame.jpg", frame)  # 儲存影格為圖片
        print("frame captured !!")
    else:
        print("error")

    cap.release()

# 輸入 RSTP 影像串流的 URL
rtsp_url = "rtsp://192.168.50.15:8582/mjpeg/1"




import time

while True:
    time.sleep(1)
    # 呼叫函式進行擷取
    capture_frame(rtsp_url)
    # ------------------------------------------------------------------------------------------
    rekognition = boto3.client('rekognition', region_name='us-west-2',
                            aws_access_key_id='AKIAWCDYLGDONNFTKNHP', aws_secret_access_key='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')

    photo = 'captured_frame.jpg'

    with open(photo, 'rb') as image_file:
        source_bytes = image_file.read()


    detect_objects = rekognition.detect_faces(Image={'Bytes': source_bytes}, Attributes=['ALL'])

    from PIL import Image
    image = Image.open('captured_frame.jpg')
    image_width, image_height = image.size
    i = 1
    for item in detect_objects.get('FaceDetails'):
        bounding_box = item['BoundingBox']
        print('Bounding box {}'.format(bounding_box))
        width = image_width * bounding_box['Width']
        height = image_height * bounding_box['Height']
        left = image_width * bounding_box['Left']
        top = image_height * bounding_box['Top']

        left = int(left)
        top = int(top)
        width = int(width) + left
        height = int(height) + top

        box = (left, top, width, height)
        box_string = (str(left), str(top), str(width), str(height))
        print(box)
        cropped_image = image.crop(box)
        thumbnail_name = '{}.png'.format(i)
        i += 1
        cropped_image.save(thumbnail_name, 'PNG')

        face_emotion_confidence = 0
        face_emotion = None
        for emotion in item.get('Emotions'):
            if emotion.get('Confidence') >= face_emotion_confidence:
                face_emotion_confidence = emotion['Confidence']
                face_emotion = emotion.get('Type')
        print('{} - {}'.format(thumbnail_name, face_emotion))
