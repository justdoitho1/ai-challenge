import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import boto3
import numpy as np
import json
import random

model = None
client = None


# -------------------------------------------------------------------------------------
# aws key setting
access_key = ''
secret_key = ''
flow_identifier = ''
flow_alias_identifier = ''
with open('access_key.json', 'r') as f:
  keys = json.load(f)
  access_key = keys.get('access_key', '')
  secret_key = keys.get('secret_key', '')
  flow_identifier = keys.get('flow_identifier', '')
  flow_alias_identifier = keys.get('flow_alias_identifier', '')
  
  client = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-west-2',
    aws_access_key_id=access_key, # user aws access key
    aws_secret_access_key =secret_key # user aws secret key
  )
  
# -------------------------------------------------------------------------------------
# model 전역변수로 사용
if tf.io.gfile.exists('product_recommendation_model.h5'):
  model = keras.models.load_model('product_recommendation_model.h5')
# predict  
def model_predict(user_data):
  global model
  prediction = model.predict(user_data)
  return np.argmax(prediction, axis=1)

# product_name = {
#   0: [ '식기세척기 1', 'WHITE', '싱글용', '용량 : 4인분', '렌탈비용 : 23,000원'],
#   1: [ '식기세척기 2', 'PINK', '싱글용', '용량 : 3인분', '렌탈비용 : 21,000원'],
#   2: [ '식기세척기 3', 'GRAY', '4인가족용', '용량 : 8인분', '렌탈비용 : 42,000원'],
#   3: [ '식기세척기 4', 'PINK', '4인가족용', '용량 : 6인분', '렌탈비용 : 38,000원'],
#   4: [ '식기세척기 5', 'WHITE', '4인가족용', '용량 : 10인분', '렌탈비용 : 47,000원'],
#   5: [ '식기세척기 6', 'WHITE', '4인가족용', '용량 : 8인분', '렌탈비용 : 43,000원'],
#   6: [ '식기세척기 7', 'BLACK', '4인가족용', '용량 : 10인분', '렌탈비용 : 40,000원'],
#   7: [ '식기세척기 8', 'BLACK', '대가족용', '용량 : 16인분', '렌탈비용 : 55,000원'],
#   8: [ '식기세척기 9', 'YELLOW', '대가족용', '용량 : 14인분', '렌탈비용 : 58,000원'],
#   9: ['식기세척기 10', 'GRAY', '대가족용', '용량 : 18인분', '렌탈비용 : 62,000원'],
# }
product_name = {
  0: [ '식기세척기 1', 'WHITE', '싱글용', '용량 : 4인분', '렌탈비용 : 23,000원'],
  1: [ '식기세척기 2', 'PINK', '싱글용', '용량 : 3인분', '렌탈비용 : 21,000원'],
  2: [ '정수기 3', 'GRAY', '4인가족용', '용량 : 8인분', '렌탈비용 : 42,000원'],
  3: [ '정수기 4', 'PINK', '4인가족용', '용량 : 6인분', '렌탈비용 : 38,000원'],
  4: [ '정수기 5', 'WHITE', '4인가족용', '용량 : 10인분', '렌탈비용 : 47,000원'],
  5: [ '정수기 6', 'WHITE', '4인가족용', '용량 : 8인분', '렌탈비용 : 43,000원'],
  6: [ '정수기 7', 'BLACK', '4인가족용', '용량 : 10인분', '렌탈비용 : 40,000원'],
  7: [ '정수기 8', 'BLACK', '대가족용', '용량 : 16인분', '렌탈비용 : 55,000원'],
  8: [ '정수기 9', 'YELLOW', '대가족용', '용량 : 14인분', '렌탈비용 : 58,000원'],
  9: ['정수기 10', 'GRAY', '대가족용', '용량 : 18인분', '렌탈비용 : 62,000원'],
}
product_img = {
  0: './img/white_1.jpg',
  1: './img/pink_1.jpg',
  2: './img/gray_1.jpg',
  3: './img/pink_2.jpg',
  4: './img/white_2.jpg',
  5: './img/white_3.jpg',
  6: './img/black_1.jpg',
  7: './img/black_2.jpg',
  8: './img/yellow_1.jpg',
  9: './img/gray_2.jpg',
}

#디스크의 파일에서 바이트 로드하기
def get_bytes_from_file(file_path):
  with open(file_path, "rb") as image_file:
      file_bytes = image_file.read()
  return file_bytes

class ChatMessage(): #이미지 및 텍스트 메시지를 저장할 수 있는 클래스를 만듭니다.
  def __init__(self, role, message_type, text, bytesio=None, image_bytes=None):
    self.role = role
    self.message_type = message_type
    self.text = text
    self.bytesio = bytesio #used for streamlit rendering
    self.image_bytes = image_bytes #used to pass to the model

def chat_with_model(message_history, new_text=None):
  if client is None:
    raise ValueError("AWS client is not initialized. Please check your AWS credentials and configuration.")  
# 사용자 입력부분(챗봇 input) -------------------------------------------------------------------
  question = new_text
  print("질문:", question)
  new_text_message = ChatMessage('user', 'text', text=new_text)
  message_history.append(new_text_message)  
  
  response = client.invoke_flow(
    flowIdentifier=flow_identifier,
    flowAliasIdentifier=flow_alias_identifier,
    inputs=[
      {
        "content": {
          "document": question
        },
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document"
      }
    ]
  )
  
  # 모델 출력부분(챗봇 output) -------------------------------------------------------------------
  result = {}

  for event in response.get("responseStream"):
    result.update(event)
  '''
  expect output format
    ```json
    {
      "output_data": [
        45,
        7,
        40,
        14,
        85,
        7
      ]
    }
    ```
  '''
  # parsing
  res = result['flowOutputEvent']['content']['document'].replace('`', '').replace('json', '')
  
  # json 문자열을 실제 json 객체로 변환
  try:
    res_json = json.loads(res)
    if 'output_data' in res_json:
      output_data = res_json['output_data']
      if len(output_data) == 6:
        # '나이', '가족 수', '렌탈비용(천원)', '용량', '만족도', '할인율'
        if(output_data[0] is None or output_data[0] == 0):
          output_data[0] = random.randint(23, 70)  # 나이
        if(output_data[4] is None or output_data[4] == 0):
          output_data[4] = random.randint(70, 95)
        if(output_data[5] is None or output_data[5] == 0):
          output_data[5] = random.randint(5, 10)
          
        user_data = np.array([output_data])
        pred_idx = model_predict(user_data.astype(int))
        result = product_name[pred_idx[0]]
        msg = "이 제품을 추천드려요 : " + str(result)

        print("이 제품을 추천드려요 : {}".format(product_name[pred_idx[0]]))
        response_message = ChatMessage('assistant', 'text', msg)
        
        img_bytes = get_bytes_from_file(product_img[pred_idx[0]])
        
        response_img = ChatMessage('assistant', 'image', text="추천 제품 이미지", bytesio=img_bytes)
        message_history.append(response_message)
        message_history.append(response_img)

        return message_history

      else:
        print("output_data의 길이가 올바르지 않습니다. 예상 길이: 6, 실제 길이: ".format(len(output_data)))
        response_message = ChatMessage('assistant', 'text', "output_data의 길이가 올바르지 않습니다.")
        return message_history.append(response_message)

    else:
      print("output_data 키가 JSON에 없습니다.")
      response_message = ChatMessage('assistant', 'text', "output_data 키가 JSON에 없습니다.")
      return message_history.append(response_message)
  except json.JSONDecodeError as e:
    print("JSON 파싱 오류:", e)
    response_message = ChatMessage('assistant', 'text', "JSON 파싱 오류가 발생했습니다.")
    return message_history.append(response_message)

# -------------------------------------------------------------------------------------

'''
if tf.io.gfile.exists('product_recommendation_model.h5'):
  model = keras.models.load_model('product_recommendation_model.h5')
  while True:
    # 사용자 입력부분(챗봇 input) -------------------------------------------------------------------
    question = input("질문을 입력하세요. 종료하고 싶으시면 exit를 입력하세요. : ")
    if question.lower() == 'exit':
      break
    client = boto3.client(
      service_name='bedrock-agent-runtime',
      region_name='us-west-2',
      aws_access_key_id=access_key, # user aws access key
      aws_secret_access_key =secret_key # user aws secret key
    )
    response = client.invoke_flow(
      flowIdentifier=flow_identifier,
      flowAliasIdentifier=flow_alias_identifier,
      inputs=[
        {
          "content": {
            "document": question
          },
          "nodeName": "FlowInputNode",
          "nodeOutputName": "document"
        }
      ]
    )
    
    # 모델 출력부분(챗봇 output) -------------------------------------------------------------------
    result = {}

    for event in response.get("responseStream"):
      result.update(event)
    # expect output format
    #   ```json
    #   {
    #     "output_data": [
    #       45,
    #       7,
    #       40,
    #       14,
    #       85,
    #       7
    #     ]
    #   }
    #   ```
    # parsing
    res = result['flowOutputEvent']['content']['document'].replace('`', '').replace('json', '')
    
    # json 문자열을 실제 json 객체로 변환
    try:
      res_json = json.loads(res)
      if 'output_data' in res_json:
        output_data = res_json['output_data']
        if len(output_data) == 6:
          # '나이', '가족 수', '렌탈비용(천원)', '용량', '만족도', '할인율'
          if(output_data[0] is None or output_data[0] == 0):
            output_data[0] = random.randint(23, 70)  # 나이
          if(output_data[4] is None or output_data[4] == 0):
            output_data[4] = random.randint(70, 95)
          if(output_data[5] is None or output_data[5] == 0):
            output_data[5] = random.randint(5, 10)
            
          print("output_data:", output_data)
          user_data = np.array([output_data])
          pred_idx = model_predict(user_data.astype(int))
          print("이 제품을 추천드려요 : {}".format(product_name[pred_idx[0]]))
        else:
          print("output_data의 길이가 올바르지 않습니다. 예상 길이: 6, 실제 길이: {}".format(len(output_data)))
      else:
        print("output_data 키가 JSON에 없습니다.")
    except json.JSONDecodeError as e:
      print("JSON 파싱 오류:", e)
      
'''