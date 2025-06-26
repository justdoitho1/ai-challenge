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

# predict  
def model_predict(user_data):
  global model
  prediction = model.predict(user_data)
  return np.argmax(prediction, axis=1)

product_name = {
  0: [ '식기세척기 1', 0xFFFFFF, '싱글용', '용량 : 4인분', '렌탈비용 : 23,000원'],
  1: [ '식기세척기 2', 0xFF0000, '싱글용', '용량 : 3인분', '렌탈비용 : 21,000원'],
  2: [ '식기세척기 3', 0x00FF00, '4인가족용', '용량 : 8인분', '렌탈비용 : 42,000원'],
  3: [ '식기세척기 4', 0x0000FF, '4인가족용', '용량 : 6인분', '렌탈비용 : 38,000원'],
  4: [ '식기세척기 5', 0xF0F0F0, '4인가족용', '용량 : 10인분', '렌탈비용 : 47,000원'],
  5: [ '식기세척기 6', 0xFF00F0, '4인가족용', '용량 : 8인분', '렌탈비용 : 43,000원'],
  6: [ '식기세척기 7', 0xFF00F0, '4인가족용', '용량 : 10인분', '렌탈비용 : 40,000원'],
  7: [ '식기세척기 8', 0xFFFFFF, '대가족용', '용량 : 16인분', '렌탈비용 : 55,000원'],
  8: [ '식기세척기 9', 0xF0F0F0, '대가족용', '용량 : 14인분', '렌탈비용 : 58,000원'],
  9: ['식기세척기 10', 0x00FF0F, '대가족용', '용량 : 18인분', '렌탈비용 : 62,000원'],
}

# -------------------------------------------------------------------------------------

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
      