# Streamlit 라이브러리를 st라는 이름으로 불러옵니다.
# Streamlit은 Python 코드만으로 웹 애플리케이션을 쉽게 만들 수 있는 라이브러리입니다.
import streamlit as st

# PIL(Pillow) 라이브러리에서 Image 클래스를 불러옵니다.
# Pillow는 Python에서 이미지를 열고 처리할 때 사용하는 대표적인 이미지 라이브러리입니다.
from PIL import Image

# Image.open() : 이미지 파일을 열어 Image 객체로 변환합니다.
# data/example.jpg 파일을 열어서 img 변수에 저장합니다.
# data 폴더는 현재 Python 파일(app.py 등)과 같은 위치에 있어야 합니다.
img = Image.open("data/python.png")

# st.image() : 웹 화면에 이미지를 출력하는 Streamlit 함수입니다.
# img : 출력할 이미지 객체
# caption : 이미지 아래에 표시되는 설명 문장
# width=300 : 이미지의 가로 크기를 300px로 설정합니다.
st.image(img, caption="예시 이미지", width=300)

# st.audio() : 웹 화면에 오디오 플레이어를 표시하는 함수입니다.
# 지정한 mp3 파일을 재생할 수 있는 플레이어가 화면에 나타납니다.
st.audio("data/승강장발빠짐주의.mp3")

# st.video() : 웹 화면에 비디오 플레이어를 표시하는 함수입니다.
# 지정한 mp4 영상을 웹 페이지에서 바로 재생할 수 있습니다.
st.video("data/승강장발빠짐주의.mp4")