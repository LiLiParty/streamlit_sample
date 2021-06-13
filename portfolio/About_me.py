import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import altair as alt

def About_me():
    st.title("About me")

    st.header("//Basic Information")
    st.write("Name: 岡村洋希 okamura hiroki")
    st.write("Belong: 北海道大学工学部情報エレクトロニクス学科メディアネットワークコース B3")

    st.header("//Major")
    st.write("通信工学、信号処理、画像・音声・言語などのメディア処理を学んでいます。研究室次第ですが、メディア処理が専攻になりそうです（？）")

    st.header("//Research")
    st.write("まだ研究室には所属していません。今のところ、メディアダイナミクス研究室を志望しています。M進予定です。")

    st.header("//Club")
    st.write("HCPC 北海道大学競技プログラミングサークルに所属しています。アルゴリズムの勉強会等を行っています。Atcoder緑です。年内には水/青になるはず。")

    st.header("//Interest")
    st.write("未来の暮らし・インフラにとっても興味があります。１００年・２００年後の世界で生きてみたいけれど、そうはいかないので最先端のインフラの開発に携わりたい。")
    st.write("見えやすく面白い技術が好きです。画像処理・音声処理・CG処理等々に興味があります。（何でもやると面白い）")

    st.header("//Skill ＆ Certification")
    st.write("・C ・C++ ・Python ・Unity ・Arduino ・基本情報技術者 ・TOEIC 755")

    link = '[GitHub](http://github.com)'
    st.markdown(link, unsafe_allow_html=True)

def Apps_Demo():
    def Apps_demo_title():
        st.title("Apps & Demo")
        st.write("サイドバーのボタンから選択してください")
        st.header("・Joycon-Tennis")
        st.write("Unityで作った、ArduinoとJoyconで操作するテニスゲームの紹介です")
        st.header("・HRTF 3DSounds demo")
        st.write("頭部伝達関数を用いた立体音響のコードです")
        st.header("・streamlit Demo ~yfinance~")
        st.write("streamlitでのAPIの練習です。株価可視化アプリになっています。")
        st.header("・Azure Computer Vision Demo")
        st.write("Azureのデモです。画像URLを入力すると物体検出します。")
    def Apps_demo_yfinance():
        st.title("Stock Price test")
        try:
            st.sidebar.write("""
            # Stockprice
            以下のオプションから表示日数を指定できます。
            """)

            st.sidebar.write("""
            ## 表示日数選択
            """)

            days = st.sidebar.slider('日数', 1, 50, 20)

            st.write(f"""
            ### 過去**{days}**日間の株価
            """)

            tickers = {
                'apple': 'AAPL',
                'facebook': 'FB',
                'google': 'GOOGL',
                'microsoft': 'MSFT',
                'netflix': 'NFLX',
                'amazon': 'AMZN'
            }
            @st.cache
            def get_data(days, tickers):
                df = pd.DataFrame()
                for company in tickers.keys():
                    tkr = yf.Ticker(tickers[company])
                    hist = tkr.history(period = f'{days}d')
                    hist.index = hist.index.strftime('%d %B %Y')
                    hist = hist[['Close']]
                    hist.columns = [company]
                    hist = hist.T
                    hist.index.name = 'Name'
                    df = pd.concat([df, hist])
                return df

            st.sidebar.write("""
            ## 株価の範囲指定
            """)
            ymin, ymax = st.sidebar.slider(
                '範囲を指定してください',
                0.0, 4000.0, (0.0,3500.0)
            )

            df = get_data(days,tickers)

            companies = st.multiselect(
                '会社名を選択',
                list(df.index),
                ['google','amazon','facebook','apple']
            )

            if not companies:
                st.error('1社以上選択してください')
            else:
                data = df.loc[companies].sort_index()
                data = data.T.reset_index()
                data = pd.melt(data, id_vars=['Date']).rename(
                    columns = {'value': 'Stock Prices(USD)'}
                )
                chart = (
                    alt.Chart(data)
                    .mark_line(opacity=0.8, clip=True)
                    .encode(
                        x='Date:T',
                        y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin,ymax])),
                        color='Name:N'
                        )
                )
                st.altair_chart(chart, use_container_width=True)
        except:
            st.error(
                "Error"
            )
    def Apps_demo_Azure():
        from azure.cognitiveservices.vision.computervision import ComputerVisionClient
        from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
        from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
        from msrest.authentication import CognitiveServicesCredentials

        from array import array
        import os
        import io
        import urllib.request
        import time
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont
        import streamlit as st
        from streamlit.type_util import is_altair_chart

        #st.title("Delete APIKEY")
        KEY = st.secrets['API_KEY']
        ENDPOINT = st.secrets['API_ENDPOINT']
        
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
        st.write("画像をアップロードするか、URLを入力してください。")

        
        upload_file = st.file_uploader(
            'Choose an image  現在こちらは正常に動かないことがあります。尚、アップロードした画像はネットワーク上に保存されますが、削除も可能です。',
            type=['png','jpg','jpeg'],
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

                    #font = ImageFont.truetype(font='Helvetica 400.ttf', size=50)
                    #text_w,text_h = draw.textsize(caption, font=font)
                    

                    draw.rectangle([(x,y),(x+w, y+h)], fill=None, outline='green', width=8)
                    #draw.rectangle([(x,y),(x+text_w, y+text_h)], fill='green')
                    draw.text((x,y), caption, fill='white')
                    
                
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
                        latest_iteration.text(f"load {i+1}")
                        bar.progress(i + 1)
                        time.sleep(0.01)
                    "Delete!!"
                    
                    upload_file = None
                    shutil.rmtree('./img')
                    os.mkdir('./img')
                    flag = 0
                    a = False
            except:
                st.error("アップロードした画像は現在扱えません！")
        

        img_url = st.text_input('Enter some URL of image',value="https://images.unsplash.com/photo-1621570168297-bdcdd4457664?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=667&q=80")

        if img_url is not None:
            try:
                f = io.BytesIO(urllib.request.urlopen(img_url).read())
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

                    font = ImageFont.truetype(font='Helvetica 400.ttf', size=30)
                    text_w,text_h = draw.textsize(caption,font=font)
                    

                    draw.rectangle([(x,y),(x+w, y+h)], fill=None, outline='green', width=8)
                    draw.rectangle([(x,y),(x+text_w, y+text_h)], fill='green')
                    draw.text((x,y), caption, fill='white',font=font)
                
            
                st.image(img)

                tags_name = get_tags_remote(img_url)
                tags_name = ', '.join(tags_name)
                st.markdown('*detected contents tag*')
                st.markdown(f'>{tags_name}')
            except:
                st.error("正しいURLを入力してください！もし正しいURLを入力してもこの表示が消えない場合は、何らかのエラーが起きています。すみません。")
    
    
    App_contents = st.sidebar.radio("",["contents","Joycon-Tennis","HRTF 3DSounds Demo","yfinance","Azure Computer Vision Demo"])
    if(App_contents == "contents"):
        Apps_demo_title()
    elif App_contents == "yfinance": 
        Apps_demo_yfinance()
    elif App_contents == "Azure Computer Vision Demo":
        Apps_demo_Azure()
    else:
        st.write("作成中です")


st.sidebar.title("About me")
st.sidebar.write("自己紹介")
st.sidebar.title("Apps & Demo")
st.sidebar.write("つくったいろいろ(順次公開予定?)")

contents = st.sidebar.radio("",["About me","Apps & Demo"])
if(contents == "About me"):
    About_me()
else:
    Apps_Demo()

st.sidebar.write(" ")
st.sidebar.write("更新 2021/06/13")

