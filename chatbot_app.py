import streamlit as st #모든 streamlit 명령은 "st" 별칭을 통해 사용할 수 있습니다
import chatbot as chat
# --------------------------------------------------------------------------------
# 그래프 임시 표시
import matplotlib.pylab as plt
import numpy as np

def plot_graph():
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')


  def convex(x, y):
    return x**2 + y**3

  X = np.arange(-10.0, 10.0, 1.0)
  Y = np.arange(-10.0, 10.0, 1.0)
  X, Y = np.meshgrid(X, Y)
  R = convex(X, Y)
  surf = ax.plot_surface(X, Y, R, cmap='viridis', edgecolor='none', label='convex function')

  fig.colorbar(surf)
  return plt

def plot_graph2():
  plt.figure()
  x = np.arange(-5, 5, 0.1)
  y = 1 / (1 + np.exp(-x))
  plt.plot(x, y)
  plt.ylim(-0.1, 1.1)
  return plt
# --------------------------------------------------------------------------------
st.set_page_config(layout="wide") # UI 가독성이 좋게

st.set_page_config(page_title="WoongDalSaem_Chatbot") #HTML 제목
st.title("스마트 웅달샘") #page 제목

tab1, tab2 = st.tabs(["제품 추천", "통계 정보 보기"]) #두 개의 탭을 만듭니다.

with tab1:
  st.header("고민고민 하지마~ (ㅇ_<)V") #tab1 헤더
  if 'chat_history' not in st.session_state: #채팅 기록이 아직 생성되지 않았는지 확인합니다.
    st.session_state.chat_history = [] #채팅 기록 초기화


  chat_container = st.container()

  input_text = st.chat_input("당신의 봇과 여기서 대화하세요") #채팅 입력 상자를 표시합니다.


  if input_text: #run the code in this if block after the user submits a chat message
    chat.chat_with_model(message_history=st.session_state.chat_history, new_text=input_text)


  #채팅 기록 다시 렌더링(Streamlit은 이 스크립트를 다시 실행하므로 이전 채팅 메시지를 보존하려면 이 기능이 필요합니다.)
  for message in st.session_state.chat_history: #채팅 기록을 반복합니다.
    with chat_container.chat_message(message.role): #주어진 역할에 대한 채팅 줄을 렌더링하고, with 블록의 모든 내용을 포함합니다.
      if (message.message_type == 'image'):
        st.image(message.bytesio)
      else:
        st.markdown(message.text) #display the chat content
                
with tab2:
  # text_to_sql
  st.header("통계 정보 보기") #tab2 헤더
  st.write("아직 준비 중입니다.") #tab2 내용
  
  graph_container = st.container()
  st.pyplot(plot_graph()) #Streamlit에 그래프를 표시합니다.
  st.pyplot(plot_graph2()) #Streamlit에 그래프를 표시합니다.