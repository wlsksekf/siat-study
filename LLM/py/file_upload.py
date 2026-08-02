import streamlit as st  # Streamlit 라이브러리를 st라는 이름으로 불러옵니다.

# st.file_uploader()
# 사용자가 파일을 업로드할 수 있는 위젯을 생성합니다.
# "파일 업로드" : 화면에 표시될 라벨
# type=["csv", "txt"] : 업로드 가능한 파일 형식을 제한합니다.
uploaded_file = st.file_uploader("파일 업로드", type=["csv", "txt"])

# uploaded_file이 None이 아니라면 (즉, 사용자가 파일을 업로드했다면)
if uploaded_file is not None:

    # 업로드된 파일의 이름을 화면에 출력합니다.
    st.write("파일 이름:", uploaded_file.name)

    st.write(f"파일 크기: {uploaded_file.size} Bytes")

    st.write("파일 타입:", uploaded_file.type)

    # uploaded_file.read()
    # 업로드된 파일의 내용을 바이트(byte) 형태로 읽습니다.
    # decode("utf-8")을 사용하여 바이트 데이터를 문자열로 변환합니다.
    content = uploaded_file.read().decode("utf-8")

    # st.text()
    # 텍스트 형식으로 파일 내용을 화면에 출력합니다.
    st.text(content)