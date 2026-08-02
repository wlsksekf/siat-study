import streamlit as st

# 체크박스 : 동의 여부
agree = st.checkbox("동의하십니까?")

# 라디오 버튼 : 성별 선택
gender = st.radio("성별을 선택하세요", ["남성", "여성"])

# 셀렉트박스 : 색상 선택
color = st.selectbox("좋아하는 색상", ["빨강", "파랑", "초록"])

# 구분선
st.divider()

# 결과 출력 영역 제목
st.markdown("### 입력 결과")

st.markdown(f"""
- 동의 여부 : **{'동의함' if agree else '동의하지 않음'}**
- 성별 : **{gender}**
- 좋아하는 색상 : **{color}**
""")