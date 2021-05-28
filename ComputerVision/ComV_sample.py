from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import io
import requests
import urllib.request
import shutil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import time
import streamlit as st
from streamlit.type_util import is_altair_chart

#st.title("Delete APIKEY")
KEY = st.secrets['API_KEY']
ENDPOINT = st.secrets['END_POINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(image_path):
    local_image = open(image_path, "rb")
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result_local.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

def get_tags_remote(img_url):
    tags_result_remote = computervision_client.tag_image(img_url)
    tags = tags_result_remote.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

def detect_objects(image_path):
    local_image = open(image_path, "rb")
    detect_objects_results_remote = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results_remote.objects
    return objects

def detect_objects_remote(img_url):
    detect_objects_results_remote = computervision_client.detect_objects(img_url)
    objects = detect_objects_results_remote.objects
    return objects


def detect_adult(image_path):
    local_image = open(image_path, "rb")
    remote_image_features = ["adult"]
    detect_adult_results = computervision_client.analyze_image_in_stream(local_image, remote_image_features)
    return detect_adult_results

def detect_adult_remote(img_url):
    remote_image_features = ["adult"]
    detect_adult_results_remote = computervision_client.analyze_image(img_url, remote_image_features)
    return detect_adult_results_remote.adult.is_adult_content



st.title("ComputerVision Sample")

upload_file = st.file_uploader(
    'Choose an image  !!!!!現在こちらは正常に動きません、下のURLを入力して実行してください!!!!!',
    type=['png','jpg','jpeg']
    )


if upload_file is not None:
    try:
        img = Image.open(upload_file)
        img_path = f'img/{upload_file.name}'
        img.save(img_path)

        if detect_adult(img_path).adult.is_adult_content:
            st.warning("！！！！これはエッチな画像です！！！！")

        objects = detect_objects(img_path)

        #描画
        draw = ImageDraw.Draw(img)
        
        for object in objects:
            x = object.rectangle.x
            y = object.rectangle.y
            w = object.rectangle.w
            h = object.rectangle.h
            caption = object.object_property

            font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
            text_w,text_h = draw.textsize(caption, font=font)
            

            draw.rectangle([(x,y),(x+w, y+h)], fill=None, outline='green', width=8)
            draw.rectangle([(x,y),(x+text_w, y+text_h)], fill='green')
            draw.text((x,y), caption, fill='white',font=font)
            
        
        st.image(img)

        tags_name = get_tags(img_path)
        tags_name = ', '.join(tags_name)
        st.markdown('*detected contents tag*')
        st.markdown(f'>{tags_name}')

        st.write("アップロード後このボタンを押すとネットワーク上のフォルダから削除されます。")

        a = st.button("Delete the folder!")
        flag = 0
        latest_iteration = st.empty()
        bar = st.progress(0)

        if a:
            flag = 1
            for i in range(100):
                latest_iteration.text(f"Iteration {i+1}")
                bar.progress(i + 1)
                time.sleep(0.01)
            "Delete!!"
            
            upload_file = None
            shutil.rmtree('./img')
            os.mkdir('./img')
            flag = 0
            a = False
    except:
        st.error("アップロード機能は現環境では動きません！")

img_url = st.text_input('Enter some URL of image',value="https;//example_of_img.jpg")

if img_url is not None:
    try:
        f = io.BytesIO(requests.get(img_url).content)
        img = Image.open(f)

        if detect_adult_remote(img_url):
            st.warning("！！！！これはエッチな画像です！！！！")

        objects = detect_objects_remote(img_url)

        #描画
        draw = ImageDraw.Draw(img)
    
        for object in objects:
            x = object.rectangle.x
            y = object.rectangle.y
            w = object.rectangle.w
            h = object.rectangle.h
            caption = object.object_property

            font = ImageFont.truetype(font='./Helvetica 400.ttf', size=30)
            text_w,text_h = draw.textsize(caption, font=font)
            

            draw.rectangle([(x,y),(x+w, y+h)], fill=None, outline='green', width=8)
            draw.rectangle([(x,y),(x+text_w, y+text_h)], fill='green')
            draw.text((x,y), caption, fill='white',font=font)
        
    
        st.image(img)

        tags_name = get_tags_remote(img_url)
        tags_name = ', '.join(tags_name)
        st.markdown('*detected contents tag*')
        st.markdown(f'>{tags_name}')

    except:
        st.error("正しいURLを入力してください")
