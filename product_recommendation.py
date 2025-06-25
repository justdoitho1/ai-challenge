import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

model = None

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
    epochs=100,
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
  0: [ '식기세척기 1', 0xFFFFFF, '싱글용', '4인분'],
  1: [ '식기세척기 2', 0xFF0000, '싱글용', '3인분'],
  2: [ '식기세척기 3', 0x00FF00, '4인가족용', '8인분'],
  3: [ '식기세척기 4', 0x0000FF, '4인가족용', '6인분'],
  4: [ '식기세척기 5', 0xF0F0F0, '4인가족용', '10인분'],
  5: [ '식기세척기 6', 0xFF00F0, '4인가족용', '8인분'],
  6: [ '식기세척기 7', 0xFF00F0, '4인가족용', '10인분'],
  7: [ '식기세척기 8', 0xFFFFFF, '대가족용', '16인분'],
  8: [ '식기세척기 9', 0xF0F0F0, '대가족용', '14인분'],
  9: ['식기세척기 10', 0x00FF0F, '대가족용', '18인분'],
}

def predict():
  # input_data = "4인 가족이 사용할 제품을 추천해주세요. 나이는 30대 중반입니다. 렌탈료는 3만원 정도가 좋겠어요."
  # 예시 문장 집합 (실제 사용시 제품 설명, 사용자 유형 등과 연결 필요)
  # columns = ['나이', '가족 구성원', '렌탈비용', '용량', '만족도', '할인율', '제품코드']
  def model_predict(user_data):
    global model
    prediction = model.predict(user_data)
    return np.argmax(prediction, axis=1)
  
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
  predict()
else:
  data = np.loadtxt('user_data.csv', delimiter=',', converters=int, dtype=int, encoding='UTF8')
  train_data = data[:, 0:-1].astype(int) # 마지막 열을 제외한 나머지 열이 사용자 데이터
  train_label = data[:,-1].astype(int) # 마지막 열이 레이블
  data_size = len(data)  # 전체 데이터 크기
  col_size = len(data[0]) - 1  # 마지막 열은 레이블이므로 제외
  np.random.seed(42)
  model_train()