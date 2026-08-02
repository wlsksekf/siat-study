import streamlit as st

# st.sidebar : 웹 화면의 왼쪽에 있는 사이드바 영역을 의미합니다.
# sidebar.title() : 사이드바에 큰 제목을 출력합니다.
st.sidebar.title("사이드바 메뉴")

# sidebar.selectbox() : 여러 개의 선택지 중 하나를 선택할 수 있는 드롭다운 메뉴를 생성합니다.
# 첫 번째 인자 : 사용자에게 보여줄 질문 또는 설명
# 두 번째 인자 : 선택 가능한 옵션 리스트
choice = st.sidebar.selectbox("선택하세요", ["옵션1", "옵션2"])

# st.write() : Streamlit에서 데이터를 화면에 출력하는 함수입니다.
# 사용자가 사이드바에서 선택한 값을 화면에 표시합니다.
st.write("선택한 옵션:", choice)