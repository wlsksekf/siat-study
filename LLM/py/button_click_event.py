import streamlit as st  # Streamlit 라이브러리를 st라는 이름으로 불러옵니다.

# st.button("Click me")
# 웹 화면에 "Click me"라는 버튼을 생성합니다.
# 버튼이 눌리면 True를 반환하고, 눌리지 않으면 False를 반환합니다.
if st.button("Click me"):

    # 버튼을 클릭하면 아래 메시지가 웹 화면에 출력됩니다.
    st.write("버튼 클릭!")