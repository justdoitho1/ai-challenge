import streamlit as st

st.set_page_config(layout="centered", page_title="Chatbot Home")

st.sidebar.image("img/wj_logo.jpg", use_container_width=True)

# 2개 컬럼으로 title + 로고 나란히 배치
title1, title2 = st.columns([6, 3])  # 비율 조정 (텍스트:이미지)

with title1:
    st.title("웅달샘 스마트 챗봇")

with title2:
    # 🔁 채팅 초기화 버튼
    if st.button("💬 채팅 초기화"):
        st.session_state["chat_history_customer"] = []  # 고객용 채팅 기록 초기화
        st.session_state["chat_history_employee"] = []  # 직원용 채팅 기록 초기화


st.write("또또사랑~ 당신은 누구신가요?")


col1, col2 = st.columns(2)

with col1:
    if st.button("👤 고객"):
        st.switch_page("pages/1_customer.py")  # customer 페이지로 이동

with col2:
    if st.button("👨‍💼 직원"):
        st.switch_page("pages/2_employee.py")  # employee 페이지로 이동
