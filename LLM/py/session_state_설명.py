import streamlit as st

# st.session_state 는 Streamlit이 제공하는 특별한 객체입니다.
# 앱이 다시 실행되더라도 값을 유지할 수 있는 상태 저장 공간입니다.

# 이 객체는 두 가지 방식으로 접근할 수 있습니다.

# 1.속성 방식
# st.session_state.count

# 2.딕셔너리 방식
# st.session_state["count"]

# 두 문법 모두 같은 값에 접근하는 것입니다.


# count 값을 0으로 초기화합니다.
# 하지만 Streamlit은 버튼을 누를 때마다 전체 코드가 다시 실행됩니다.
# 그래서 버튼을 누를 때마다 count 값이 다시 0으로 설정됩니다.
st.session_state.count = 0


# Streamlit은 리액티브(reactive) 앱 프레임워크입니다.
# 일반적인 Python 스크립트와 달리 사용자 인터랙션(버튼, 입력 등)에 반응하여
# 앱 전체 코드를 위에서 아래로 다시 실행합니다.

# st.button("증가") : "증가" 버튼을 화면에 생성합니다.
# 사용자가 버튼을 클릭하면 True가 되어 if 블록이 실행됩니다.

if st.button("증가"):

    # 버튼 클릭 시 count 값을 1 증가시킵니다.
    st.session_state.count += 1

    # 증가된 값을 화면에 출력합니다.
    st.write(st.session_state.count)