# Streamlit 라이브러리 불러오기
# 웹 애플리케이션을 Python 코드만으로 쉽게 만들 수 있는 라이브러리입니다.
import streamlit as st


# st.write()
# Streamlit에서 가장 기본적인 출력 함수입니다.
# 문자열, 숫자, 리스트, 데이터프레임, 이미지 등 다양한 객체를 화면에 출력할 수 있습니다.

# 문자열 출력
st.write("안녕하세요")


# 리스트 출력
# Python 리스트를 그대로 화면에 표시합니다.
st.write([1, 2, 3])


# pandas 라이브러리 불러오기
# 데이터 분석에서 가장 많이 사용하는 라이브러리입니다.
# 설치 명령어 : pip install pandas
import pandas as pd


# pandas DataFrame 생성
# 딕셔너리를 이용하여 간단한 표 형태 데이터를 만듭니다.
df = pd.DataFrame({
    "a": [1, 2],  # a 열
    "b": [3, 4]   # b 열
})


# DataFrame 출력
# Streamlit은 DataFrame을 자동으로 표(table) 형태로 화면에 표시합니다.
st.write(df)


# st.image() : Streamlit에서 이미지를 화면에 표시하는 함수입니다.
# 문자열로 이미지 파일 경로를 전달하면 해당 이미지를 웹 페이지에 출력합니다.
st.image("data/python.png")
