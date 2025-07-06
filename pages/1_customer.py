import streamlit as st #모든 streamlit 명령은 "st" 별칭을 통해 사용할 수 있습니다
import chatbot as chat # 제품추천 모델
# --------------------------------------------------------------------------------

st.set_page_config(layout="centered", page_title="customer") #페이지 제목과 레이아웃 설정


# CSS 스타일 정의
st.markdown("""
    <style>
    /* 첫 번째 헤더: 배경색 대신 이미지 넣기 */
    .header1 {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 40px;
        background-color: white;  /* 이미지 투명 부분 보일 때 */
        display: flex;
        align-items: center;
        padding-left: 10px;  /* 이미지 왼쪽 간격 */
        z-index: 100;
    }

    .header1 img {
        height: 30px;  /* 헤더 높이에 맞게 이미지 크기 조절 */
    }

    /* 두 번째 헤더: 타이틀 표시 */
    .header2 {
        position: fixed;
        top: 40px;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: #F2811D;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        z-index: 99;
    }

    /* 본문과 헤더가 겹치지 않도록 여백 확보 */
    .content {
        margin-top: 110px;
        padding: 20px;
    }
    </style>

    <!-- 실제 헤더 영역 -->
    <div class="header1"></div>
    <div class="header2">💖 웅달샘 고객 챗봇</div>
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

st.subheader("원하시는 제품을 말씀해주세요 V(ㅇㅅ<)V") #tab1 헤더

CHAT_KEY = "chat_history_customer"

if CHAT_KEY not in st.session_state: #채팅 기록이 아직 생성되지 않았는지 확인합니다.
    st.session_state[CHAT_KEY] = [] #채팅 기록 초기화

chat_container = st.container()

# 입력창 + 초기화 버튼을 한 줄에
col1, col2 = st.columns([4, 1])  # 비율 조정 가능

with col1:
    input_text = st.chat_input("또또사랑~ 달샘이에게 물어봐주세요~", key="user_input") #채팅 입력 상자를 표시합니다.

with col2:
    if st.button("💬 초기화"):
        st.session_state[CHAT_KEY] = []
        st.rerun()  # 화면 즉시 갱신

if input_text: #run the code in this if block after the user submits a chat message
  chat.chat_with_model(message_history=st.session_state[CHAT_KEY], new_text=input_text)

#채팅 기록 다시 렌더링(Streamlit은 이 스크립트를 다시 실행하므로 이전 채팅 메시지를 보존하려면 이 기능이 필요합니다.)
for message in st.session_state[CHAT_KEY]: #채팅 기록을 반복합니다.
  with chat_container.chat_message(message.role): #주어진 역할에 대한 채팅 줄을 렌더링하고, with 블록의 모든 내용을 포함합니다.
    if message.role == "user":
      st.markdown(f'<div class="user-bubble">{message.text}</div>', unsafe_allow_html=True)
    elif message.role == "assistant":
      if message.message_type == "text":
        st.markdown(f'<div class="assistant-bubble">{message.text}</div>', unsafe_allow_html=True)
      elif message.message_type == "image" and message.bytesio:
        st.image(message.bytesio, caption="제품 이미지")
      

