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
    st.write("通信工学、信号処理、画像・音声・言語などのメディア処理を学んでいます。研究室次第ですが、メディア処理が専攻になりそうです。")

    st.header("//Research")
    st.write("まだ研究室には所属していません。今のところ、メディアダイナミクス研究室を志望しています。M進予定です。")

    st.header("//Club")
    st.write("HCPC 北海道大学競技プログラミングサークルに所属しています。アルゴリズムの勉強会等を行っています。Atcoder緑です。年内には水/青になるはず。")

    st.header("//Interest")
    st.write("未来の暮らし・インフラにとっても興味があります。１００年・２００年後の世界で生きてみたいけれど、そうはいかないので最先端のインフラの開発に携わりたい。")
    st.write("見えやすい、面白い、未来感のある技術が好きです。画像処理・音声処理・CG処理等々に興味があります。（何でもやると面白いけれど、、）")

    st.header("//Skill ＆ Certification")
    st.write("・C ・C++ ・Python ・Unity ・Arduino ・基本情報技術者 ・TOEIC 755")

    st.header("//Link")
    link_1 = '[メディアネットワークコース - 学科・コース | 北大工](https://www.eng.hokudai.ac.jp/course/?c=2040)'
    st.markdown(link_1, unsafe_allow_html=True)
    link_2 = '[HCPC 北海道大学競技プログラミングサークル](https://hcpc-hokudai.github.io/)'
    st.markdown(link_2, unsafe_allow_html=True)
    link_3 = '[北海道大学 大学院情報科学研究院 メディアダイナミクス研究室](https://www-lmd.ist.hokudai.ac.jp/)'
    st.markdown(link_3, unsafe_allow_html=True)

    #link = '[GitHub](http://github.com)'
    #st.markdown(link, unsafe_allow_html=True)

def Apps_Demo():
    def Apps_demo_title():
        st.title("Apps & Demo")
        st.write("サイドバーのボタンから選択してください")
        st.header("・Joy-Con Tennis")
        st.write("Unityで作った、ArduinoとJoyconで操作するテニスゲームの紹介です")
        st.header("・HRTF 3DSounds ")
        st.write("頭部伝達関数を用いた立体音響のコードです")
        st.header("・streamlit Demo ~yfinance~")
        st.write("streamlitでのAPIの練習です。株価可視化アプリになっています。")
        st.header("・Azure Computer Vision Demo")
        st.write("Azureのデモです。画像URLを入力すると物体検出します。")
        st.write("")
        st.write("順次、他のプログラムもWebアプリ化したい。")
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
    def Apps_demo_Unity():
        st.title("Joy-Con Tennis")
        st.write("Nintendo SwitchのJoy-ConとArduinoで操作できるテニスゲームを作りました。JoyconLibというものを使っています。")
        st.write("Unityを趣味で触っている時に、ちょうど大学でArduinoを用いたチーム自由制作があったので発表まで仕上げました。コース内で一位をいただきました。")
        st.image("instrument_name.png")
        st.error("大きめの音が出ます。")
        st.video("Joy-Con Tennis.mp4")
        #st.write("メディアネットワーク演習という講義でした。Youtubeに紹介動画が上がっています。")
    def Apps_demo_hrtf():
        st.title("HRTF 3DSounds")
        st.write("HRTFの畳み込みによる立体音響を試したものです。音源.wav を 右から左に移動する音源.wav として書き出します。")
        st.write("人間は、音源の方向を左右の耳から聞こえる音の差異で判断しています。これを音源定位と呼びますが、心理的なもの・音圧差・位相差などに影響されています。")
        st.write("このプログラムでは、HRTF(頭部伝達関数)を音源に畳み込むことによって音源を移動させています。HRTFは、頭部及び体によって生じる音の変化を伝達関数として表したものです。")
        st.write("名古屋大学のHRTFデータベースを用いました。右から左の移動方向のHRTFを順次畳み込んでいくのですが、少し音飛びしてしまっています、、、")
        st.audio("hrtf_siren.wav")
        """
        ヘッドホンをしてお聞きください。念の為、小さい音量から聞いてください。
        """
        link_1 = '[Head Related Transfer Functions (http://www.sp.m.is.nagoya-u.ac.jp/HRTF/index-j.html) 2021/6/14閲覧](http://www.sp.m.is.nagoya-u.ac.jp/HRTF/index-j.html)'
        st.markdown(link_1, unsafe_allow_html=True)
        link_2 = "[参考にしたサイト(https://zack-ff.hatenablog.com/entry/2017/01/05/180628) 2021/6/14閲覧](https://zack-ff.hatenablog.com/entry/2017/01/05/180628)"
        st.markdown(link_2, unsafe_allow_html=True)
        st.write("以下、プログラム(python)です。尚、変換前のサイレン音は別に作っています。")
        """
        ```python
        import numpy
        import pyaudio
        import scipy.io.wavfile as scw
        from scipy.io.wavfile import write
        import wave  
        import struct  

        def load_elev0hrtf():
            elev0Hrtf_L = {}
            elev0Hrtf_R = {}

            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                fileName = "L0e" + str_i + "a.dat"
                filePath = "./hrtfs/elev0/" + fileName
                test = open(filePath, "r").read().split("\\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                elev0Hrtf_L[i] = data

            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                fileName = "R0e" + str_i + "a.dat"
                filePath = "./hrtfs/elev0/" + fileName
                test = open(filePath, "r").read().split("\\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                elev0Hrtf_R[i] = data

            return elev0Hrtf_L, elev0Hrtf_R

        def convolution(data, hrtf, N, L):
            spectrum = numpy.fft.fft(data, n = N)
            hrtf_fft = numpy.fft.fft(hrtf, n = N)
            add = spectrum * hrtf_fft
            result = numpy.fft.ifft(add, n = N)
            return_data = result.real
            return return_data[:L], return_data[L:]

        def play_elev0(sound_data, N, L, hrtfL, hrtfR, position, overLap, streamObj):
            index = 0
            overLap_L = numpy.zeros(overLap)
            overLap_R = numpy.zeros(overLap)

            all = []

            while(sound_data[index:].size > L):
                result_data = numpy.empty((0, 2), dtype=numpy.int16)

                tmp_conv_L, add_L = convolution(sound_data[index:index + L, 0], hrtfL[position], N, L)
                tmp_conv_R, add_R = convolution(sound_data[index:index + L, 1], hrtfR[position], N, L)

                tmp_conv_L[:overLap] += overLap_L
                tmp_conv_R[:overLap] += overLap_R

                overLap_L = add_L
                overLap_R = add_R

                for i in range(tmp_conv_L.size):
                    result_data = numpy.append(result_data, numpy.array([[int(tmp_conv_L[i]), int(tmp_conv_R[i])]], dtype=numpy.int16), axis=0)

                streamObj.write(bytes(result_data))#bytes(result_data)=stream.read(CHUNK)
                all.append(bytes(result_data))

                index += L

            streamObj.close()

            wavFile = wave.open("please_last.wav", 'wb')
            wavFile.setnchannels(2)
            wavFile.setsampwidth(p.get_sample_size(8))
            wavFile.setframerate(48000)
            wavFile.writeframes(b''.join(all)) 
            wavFile.close()

        soundDataPath = "./test_10s.wav"
        rate, soundData = scw.read(soundDataPath)

        p = pyaudio.PyAudio()
        stream = p.open(format = 8,
                        channels = 2,
                        rate = rate,
                        output = True,
                        )

        hrtf_L, hrtf_R = load_elev0hrtf()
        N = 1024
        L = 513
        overLap = 511
        position = 60

        p.terminate()

        #参考https://zack-ff.hatenablog.com/entry/2017/01/05/180628
        ```
        """


    
    App_contents = st.sidebar.radio("",["contents","Joy-Con Tennis","HRTF 3DSounds","yfinance","Azure Computer Vision Demo"])
    if(App_contents == "contents"):
        Apps_demo_title()
    elif App_contents == "yfinance": 
        Apps_demo_yfinance()
    elif App_contents == "Azure Computer Vision Demo":
        Apps_demo_Azure()
    elif App_contents == "Joy-Con Tennis":
        Apps_demo_Unity()
    elif App_contents == "HRTF 3DSounds":
        Apps_demo_hrtf()
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
st.sidebar.write("更新 2021/06/14")

