import streamlit as st

st.title("Streamlit Anchor Link Example")

st.write("아래 링크를 클릭하면 Header Example 위치로 이동합니다.")

# 헤더 위치로 이동하는 링크
st.markdown("[Header Example로 이동](#header-example)")

st.write("---")

st.header("Header Example")

st.write("이 위치가 바로 앵커(anchor) 위치입니다.")

st.write("URL 예시:")
st.code("http://localhost:8501/#header-example")


# Header Example -> #header-example 이유
# 헤더 문자열 -> 소문자 + 공백을 하이픈(-)으로 변경 -> 앵커 ID 생성
# st.header("Header Example")는 내부적으로 #header-example 이라는 HTML anchor id가 만들어집니다.