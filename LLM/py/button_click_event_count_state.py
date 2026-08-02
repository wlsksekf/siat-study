import streamlit as st

# 버튼을 클릭했을 때 Streamlit에서 전체 코드가 다시 실행합니다.
# 문제: 버튼을 눌러도 이전 값이 유지되지 않으면 매번 0으로 초기화됩니다.
# 해결: st.session_state를 사용하면 값이 세션(사용자) 단위로 유지됩니다.

# count가 세션 상태에 없으면 0으로 초기화
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("증가"):
    st.session_state.count += 1

st.write(f"{st.session_state.count}번 click")