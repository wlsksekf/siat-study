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

    # 업로드된 파일의 크기를 Byte 단위로 출력합니다.
    st.write(f"파일 크기: {uploaded_file.size} Bytes")

    # 업로드된 파일의 MIME 타입을 출력합니다.
    st.write("파일 타입:", uploaded_file.type)

    # uploaded_file.read()
    # 업로드된 파일의 내용을 바이트(byte) 형태로 읽습니다.
    file_bytes = uploaded_file.read()

    # decode("utf-8")을 사용하여 바이트 데이터를 문자열로 변환합니다.
    content = file_bytes.decode("utf-8")

    # 구분선
    st.divider()

    # 업로드한 파일 내용을 화면에 출력합니다.
    st.subheader("파일 내용")
    st.text(content)

    # 구분선
    st.divider()

    # 다운로드 버튼 제목
    st.subheader("파일 다운로드")

    # st.download_button()
    # 사용자가 파일을 다운로드할 수 있는 버튼을 생성합니다.

    # mime은 파일의 형식(타입)을 나타내는 표준 문자열입니다.
    # 브라우저가 이 파일이 어떤 종류인지 알 수 있도록 알려주는 값입니다.
    # MIME type (Multipurpose Internet Mail Extensions)
    st.download_button(
        label="업로드한 파일 다운로드", # 버튼에 표시할 글자
        data=file_bytes,             # 다운로드할 실제 파일 데이터
        file_name=uploaded_file.name, # 다운로드될 파일 이름
        mime=uploaded_file.type      # 파일 타입 지정
    )