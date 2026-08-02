import streamlit as st

# count가 세션 상태에 없으면 0으로 초기화
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("증가"):
    st.session_state.count += 1

st.write(st.session_state.count)