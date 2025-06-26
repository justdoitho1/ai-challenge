import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

model = None
client = None
  
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
  
# 모델이 없으면 학습을 시작한다.    
if not tf.io.gfile.exists('product_recommendation_model.h5'):
  data = np.loadtxt('user_data.csv', delimiter=',', converters=int, dtype=int, encoding='UTF8')
  train_data = data[:, 0:-1].astype(int) # 마지막 열을 제외한 나머지 열이 사용자 데이터
  train_label = data[:,-1].astype(int) # 마지막 열이 레이블
  data_size = len(data)  # 전체 데이터 크기
  col_size = len(data[0]) - 1  # 마지막 열은 레이블이므로 제외
  np.random.seed(42)
  model_train()
  
  

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