import streamlit as st #모든 streamlit 명령은 "st" 별칭을 통해 사용할 수 있습니다
import base64
from PIL import Image
import chatbot as chat # 제품추천 모델
# --------------------------------------------------------------------------------

st.set_page_config(layout="centered", page_title="customer") #페이지 제목과 레이아웃 설정

def img_to_base64(path):
    with open(path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    return f"{img_data}"  # MIME 타입 추가

img_base64_wjCi = img_to_base64("./img/wjCi.png")
img_base64_dalsam = img_to_base64("./img/dalsam.png")
img_base64_customer = img_to_base64("./img/customer.png")

# CSS 스타일 정의
st.markdown(f"""
    <style>
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

    .header2 {{
        position: fixed;
        top: 90px; /* header0 + header1 높이만큼 내림 */
        left: 0;
        width: 100%;
        height: 60px;
        background-color: #F2811D;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 300px;
        color: white;
        font-size: 28px;
        font-weight: bold;
        z-index: 99;
    }}

    .content {{
        margin-top: 150px;
        padding: 20px;
    }}
    </style>

    <!-- 실제 헤더 영역 -->
    <div class="header0">
        <img src="data:image/png;base64,{img_base64_wjCi}" style="height: 70px;">
    </div>
    <div class="header1"></div>
    <div class="header2">
      <img src="data:image/png;base64,{img_base64_dalsam}" style="height: 50px;">
       고객님 달샘이가 도와드릴게요!
    </div>
""", unsafe_allow_html=True)

# 본문 콘텐츠
st.markdown('<div class="content">', unsafe_allow_html=True)




# --------------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .user-bubble {{
        background-color: #F2811D;
        color: white;
        padding: 0.7em 1.2em;
        border-radius: 1.2em 1.2em 0.3em 1.2em;
        margin-bottom: 0.5em;
        max-width: 60%;
        align-self: flex-end;
        font-size: 1.1em;
        box-shadow: 1px 1px 8px #b7b7b7;
    }}
    .assistant-bubble {{
        background-color: #f2f0e7;
        color: black;
        padding: 0.7em 1.2em;
        border-radius: 1.2em 1.2em 1.2em 0.3em;
        margin-bottom: 0.5em;
        max-width: 60%;
        align-self: flex-start;
        font-size: 1.1em;
        box-shadow: 1px 1px 8px #b7b7b7;
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 0.2em;
        margin-bottom: 1em;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------------------------------------

st.markdown(
    "<h3 style='color:#f35011;'>달샘이가 추천해드려요!</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='font-size: 14px; color: gray;'>고객님의 상황에 맞는 제품을 추천해드려요.</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='font-size: 14px; color: gray;'>추천 제품의 이미지를 제공해드려요.</p>",
    unsafe_allow_html=True
)

CHAT_KEY = "chat_history_customer"

if CHAT_KEY not in st.session_state: #채팅 기록이 아직 생성되지 않았는지 확인합니다.
    st.session_state[CHAT_KEY] = [] #채팅 기록 초기화

chat_container = st.container()

# 입력창 + 초기화 버튼을 한 줄에
col1, col2 = st.columns([4, 1])  # 비율 조정 가능

with col1:
    input_text = st.chat_input("또또사랑~ 달샘이에게 물어봐주세요~", key="user_input") #채팅 입력 상자를 표시합니다.

with col2:
    if st.button("💬 초기화", key="clean"):
        st.session_state[CHAT_KEY] = []
        st.rerun()  # 화면 즉시 갱신


st.markdown(
    "<p style='font-size: 13px; color: gray;'>질문은 아래 버튼을 참고하세요.</p>",
    unsafe_allow_html=True
)
# 예시 질문 목록 
question_examples = ["25살이 쓸 만한 제품을 추천해주세요. 용량은 4인분이 좋겠어요 렌탈료는 2만원 정도에요 할인은 5%정도구요 만족도는 80점 이상이면 좋겠어요 ",
                    "7명 정도가 사용할 제품을 추천해주세요. 나이는 45살이고 렌탈료는 4만원이 좋겠어요. 할인율은 7%정도, 용량은 14인분이에요. 제품을 구매한 사람의 만족도가 85점 정도면 좋겠어요"]

# 예시 질문 버튼을 생성합니다.
for i, example in enumerate(question_examples):
    if st.button(example, key=f"example_{i}"): # 예시 질문 버튼을 클릭하면 입력창에 예시 질문을 넣습니다.
        input_text = example
        

if input_text: #run the code in this if block after the user submits a chat message
  chat.chat_with_model(message_history=st.session_state[CHAT_KEY], new_text=input_text)


avatar_data_url = f"data:image/png;base64,{img_base64_customer}"
avatar_data_url2 = f"data:image/png;base64,{img_base64_dalsam}"


#채팅 기록 다시 렌더링(Streamlit은 이 스크립트를 다시 실행하므로 이전 채팅 메시지를 보존하려면 이 기능이 필요합니다.)
for message in st.session_state[CHAT_KEY]: #채팅 기록을 반복합니다.
  if message.role == "user":
    with chat_container.chat_message("user", avatar=avatar_data_url): #주어진 역할에 대한 채팅 줄을 렌더링하고, with 블록의 모든 내용을 포함합니다.
      st.markdown(f'<div class="user-bubble">{message.text}</div>', unsafe_allow_html=True)
  elif message.role == "assistant":
    with chat_container.chat_message("assistant", avatar=avatar_data_url2):
      if message.message_type == "text":
        st.markdown(f'<div class="assistant-bubble">{message.text}</div>', unsafe_allow_html=True)
      elif message.message_type == "image" and message.bytesio:
        st.image(message.bytesio, caption="제품 이미지")
      

