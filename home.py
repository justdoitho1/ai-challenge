import streamlit as st

st.set_page_config(layout="centered", page_title="Chatbot Home")

logo_url = "img/wj_logo.jpg"
st.sidebar.image(logo_url, use_container_width=True)

st.title("웅달샘 스마트 챗봇💕")
st.image(logo_url, width=500)

st.write("또또사랑~ 웅달샘 챗봇에 오신 것을 환영합니다! 💕")


col1, col2 = st.columns(2)

with col1:
    if st.button("💖 고객"):
        st.switch_page("pages/1_customer.py")  # customer 페이지로 이동

with col2:
    if st.button("💛 직원"):
        st.switch_page("pages/2_employee.py")  # employee 페이지로 이동
