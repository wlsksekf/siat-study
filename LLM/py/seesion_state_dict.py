import streamlit as st

# st.session_state.count = 10 과 같은 표현입니다.
st.session_state["count"] = 10

if st.button("증가"):
    st.session_state.count += 1
    st.write(st.session_state.count)