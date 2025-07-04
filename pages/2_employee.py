import streamlit as st #모든 streamlit 명령은 "st" 별칭을 통해 사용할 수 있습니다
from marketing_chat import marketing_chatbot_toText as chat_sql # 통계정보 보기 모델
# --------------------------------------------------------------------------------

st.set_page_config(layout="centered", page_title="employee") #페이지 제목과 레이아웃 설정
st.title("👨‍💼 직원용") # title 설정

# --------------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .user-bubble {{
        background-color: #f7624e;
        color: white;
        padding: 0.7em 1.2em;
        border-radius: 1.2em 1.2em 1.2em 0.3em;
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
        border-radius: 1.2em 1.2em 0.3em 1.2em;
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
# text_to_sql
st.header("원하시는 자료를 말씀해주세요 V(ㅇㅅ<)V") #tab2 헤더

CHAT_KEY = "chat_history_employee"

if CHAT_KEY not in st.session_state: #채팅 기록이 아직 생성되지 않았는지 확인합니다.
    st.session_state[CHAT_KEY] = [] #채팅 기록 초기화

chat_container = st.container()

input_text = st.chat_input("또또사랑~ 달샘이에게 물어봐~") #채팅 입력 상자를 표시합니다.

if input_text: #run the code in this if block after the user submits a chat message
  chat_sql.chat_with_sql(message_history=st.session_state[CHAT_KEY], new_text=input_text)

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

