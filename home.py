import streamlit as st
import base64
from PIL import Image

st.set_page_config(layout="centered", page_title="Chatbot Home")
def img_to_base64(path):
    with open(path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    return f"{img_data}"  # MIME 타입 추가

img_base64_wjCi = img_to_base64("./img/wjCi.png")
img_base64_dalsam = img_to_base64("./img/dalsam.png")
img_base64_employee = img_to_base64("./img/employee.png")
img_base64_customer = img_to_base64("./img/customer.png")

# CSS 스타일 정의
st.markdown(f"""
    <style>
    div.stButton > button {{
        font-size: 32px;  /* 글씨 크기 증가 */
        padding: 48px 120px;  /* 2em 5em을 px로 변환 */
        height: 96px;  /* 4em을 px로 변환 */
        width: 100%;
        background-color: #F58D21;
        color: white;
        border-radius: 12px;
        white-space: nowrap;
    }}
    .header0 {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 300px;
        z-index: 110;
        padding-top: 30px;
    }}

    .header0 img {{
        height: 40px;
    }}
    
    .header1 {{
        position: fixed;
        top: 50px; /* header0 높이만큼 내림 */
        left: 0;
        width: 100%;
        height: 40px;
        background-color: white;
        display: flex;
        align-items: center;
        padding-left: 7px;
        z-index: 100;
    }}

    .header1 img {{
        height: 30px;
    }}
    .content {{
        margin-top: 50px;
        padding: 20px;
    }}
    </style>

    <!-- 실제 헤더 영역 -->
    <div class="header0">
        <img src="data:image/png;base64,{img_base64_wjCi}" style="height: 70px;">
    </div>
    <div class="header1"></div>
""", unsafe_allow_html=True)

# 본문 콘텐츠
st.markdown('<div class="content">', unsafe_allow_html=True)


st.markdown(
    "<h3 style='text-align: center;color:#f35011;'>또또사랑~ 달샘이가 도와드릴게요!</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{0}' width='300'>
    </div>
    """.format(img_to_base64("./img/dalsam_2.png")),
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 3.5])


with col2:
    if st.button("고객용"):
        st.switch_page("pages/1_customer.py")  # 고객 페이지로 이동

with col4:
    if st.button("직원용"):
        st.switch_page("pages/2_employee.py")  # 직원 페이지로 이동