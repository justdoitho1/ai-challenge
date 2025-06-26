import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import boto3
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

model = None
client = None
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
  
# 모델이 이미 존재하면 불러오고, 없으면 새로 학습한다.
def model_train():
  global train_data, train_label, col_size, model, data_size
  
  index_list = np.arange(0, len(train_label))
  validation_index = np.random.choice(index_list, size=int(data_size / 10), replace=False)
  
  validating_data = train_data[validation_index]
  validating_label = train_label[validation_index]
  print("validating_data size : ", len(validating_data), validating_data.shape)
  print("validating_label size : ", len(validating_label), validating_label.shape)
  train_data = np.delete(train_data, validation_index, axis=0)  # train_data
  train_label = np.delete(train_label, validation_index, axis=0)
  print("train_data size : ", len(train_data), train_data.shape)
  print("train_label size : ", len(train_label), train_label.shape)
  
  # min-max scaling
  # min_key = np.min(train_data)
  # max_key = np.max(train_data)
  # train_data = (train_data - min_key) / (max_key - min_key)
  # validating_data = (validating_data - min_key) / (max_key - min_key)
  # train_label = (train_label - min_key) / (max_key - min_key)
  # validating_label = (validating_label - min_key) / (max_key - min_key)
  
  model = keras.models.Sequential([
    keras.Input(shape=(col_size,)),
    Dense(30, activation='elu', name="Hidden_Layer_1"),
    BatchNormalization(),
    Dropout(0.2),
    Dense(15, activation='elu', name="Hidden_Layer_2"),
    BatchNormalization(),
    Dropout(0.2),
    Dense(10, activation='softmax', name="Output_Layer")
  ])
  
  optimizer = keras.optimizers.Adam(learning_rate=0.001)
  model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
  
    # 조기 종료 조건 설정
  early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    min_delta=0.001,
    patience=10,
    restore_best_weights=True
  )
  history = model.fit(
    train_data, train_label, 
    validation_data=(validating_data, validating_label),
    epochs=60,
    batch_size=5000,
    verbose=1,
    callbacks=[early_stopping]
  )
  
  history_dict = pd.DataFrame(history.history)
  history_dict.plot(figsize=(12, 8), linewidth=3)
  plt.grid(True)
  
  plt.legend(loc='best', fontsize=15)
  plt.title("Training History", fontsize=20, pad=20)
  plt.xlabel("Epochs", fontsize=15)
  plt.ylabel("Loss/Accuracy", fontsize=15)
  
  ax = plt.gca()
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  plt.show()
  
  print(model.evaluate(validating_data, validating_label, verbose=1))
  
  model.save('product_recommendation_model.h5')

  
member_type = {
  1: '싱글',
  2: '4인가족',
  3: '대가족'
}
member_type_reverse = {
  '싱글': 1,
  '혼자': 1,
  '1인가족': 1,
  '1인 가구': 1,
  '4인 가족': 2,
  '4인 가구': 2,
  '3~4명': 2,
  '대가족': 3,
  '대가구': 3,
  '5인 가족': 3, 
  '5명 이상': 3
}

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
def model_predict(user_data):
  global model
  prediction = model.predict(user_data)
  return np.argmax(prediction, axis=1)

def predict():
  # input_data = "4인 가족이 사용할 제품을 추천해주세요. 나이는 30대 중반입니다. 렌탈료는 3만원 정도가 좋겠어요."
  # columns = ['나이', '가족 구성원', '렌탈비용', '용량', '만족도', '할인율', '설명']

  
  # 나이, 가족수, 렌탈비용, 용량, 만족도, 할인율
  user_data = np.array([
    [25, 2, 25, 5, 90, 5, "나이 - 25, 가족 수 - 2, 렌탈비용(단위 : 1000) - 25, 용량 - 5, 만족도 - 90근처, 할인율 - 5"],
    [43, 5, 45, 8, 85, 10, "나이 - 43, 가족 수 - 5, 렌탈비용(단위 : 1000) - 45, 용량 - 8, 만족도 - 85근처, 할인율 - 10"], 
    [60, 8, 60, 16, 90, 5, "나이 - 60, 가족 수 - 8, 렌탈비용(단위 : 1000) - 60, 용량 - 16, 만족도 - 90근처, 할인율 - 5"],
    [30, 3, 30, 6, 80, 10, "나이 - 30, 가족 수 - 3, 렌탈비용(단위 : 1000) - 30, 용량 - 6, 만족도 - 80근처, 할인율 - 10"],
    [50, 8, 50, 16, 85, 5, "나이 - 50, 가족 수 - 8, 렌탈비용(단위 : 1000) - 50, 용량 - 16, 만족도 - 85근처, 할인율 - 5"]
  ])
  pred_idx = model_predict(user_data[:, 0:-1].astype(int))  # 마지막 열은 제외하고 예측
  for i, idx in enumerate(pred_idx):
    print("predict product {} : {}".format(user_data[i][-1], product_name[idx]))
        
    
  
if tf.io.gfile.exists('product_recommendation_model.h5'):
  model = keras.models.load_model('product_recommendation_model.h5')
  # predict() # unit-test
  while True:
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
    
    result = {}

    for event in response.get("responseStream"):
      result.update(event)
    if result['flowCompletionEvent']['completionReason'] == 'SUCCESS':
      print(result['flowOutputEvent']['content']['document'])
    
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
          user_data = np.array([output_data])
          pred_idx = model_predict(user_data.astype(int))
          print("이 제품을 추천드려요 : {}".format(product_name[pred_idx[0]]))
        else:
          print("output_data의 길이가 올바르지 않습니다. 예상 길이: 6, 실제 길이: {}".format(len(output_data)))
      else:
        print("output_data 키가 JSON에 없습니다.")
    except json.JSONDecodeError as e:
      print("JSON 파싱 오류:", e)

    
else:
  data = np.loadtxt('user_data.csv', delimiter=',', converters=int, dtype=int, encoding='UTF8')
  train_data = data[:, 0:-1].astype(int) # 마지막 열을 제외한 나머지 열이 사용자 데이터
  train_label = data[:,-1].astype(int) # 마지막 열이 레이블
  data_size = len(data)  # 전체 데이터 크기
  col_size = len(data[0]) - 1  # 마지막 열은 레이블이므로 제외
  np.random.seed(42)
  model_train()