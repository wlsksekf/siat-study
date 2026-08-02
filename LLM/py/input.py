import streamlit as st # streamlit 라이브러리를 st라는 이름으로 불러옵니다.

# st.text_input("이름을 입력하세요")
# 웹 화면에 텍스트 입력창을 생성합니다.
name = st.text_input("이름을 입력하세요")

# st.number_input("나이를 입력하세요", min_value=0, max_value=100)
# 숫자를 입력할 수 있는 입력창을 생성합니다.
# min_value=0 -> 입력 가능한 최소값은 0
# max_value=100 -> 입력 가능한 최대값은 100
age = st.number_input("나이를 입력하세요", min_value=0, max_value=100)

st.write(f"안녕하세요 {name}님, {age}살이시네요.")