import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = np.loadtxt('user_data.csv', delimiter=',', skiprows=1, dtype=str)
np.random.seed(42)
random.shuffle(data)  # 데이터 랜덤 셔플

train_data = data[:][:-1].astype(int) # 마지막 열을 제외한 나머지 열이 사용자 데이터
train_label = data[:][-1].astype(int) # 마지막 열이 레이블
data_size = len(data[0]) - 1  # 마지막 열은 레이블이므로 제외

model = None
if tf.io.gfile.exists('product_recommendation_model.h5'):
  model = keras.models.load_model('product_recommendation_model.h5')
  

# 모델이 이미 존재하면 불러오고, 없으면 새로 학습한다.
def model_train():
  global train_data, train_label, data_size, model
  
  index_list = np.arange(0, len(train_label))
  validation_index = np.random.choice(index_list, size=5000, replace=False)
  
  validating_data = train_data[validation_index]
  validating_label = train_label[validation_index]
  
  train_data = np.delete(train_data, validation_index, axis=0)  # train_data
  train_label = np.delete(train_label, validation_index, axis=0)
  
  plt.hist([train_label, validating_label], bins=10, rwidth=0.8, label=['train', 'validating'])
  plt.title("User Data Label Distribution after splitting")
  plt.show()
  
  # min-max scaling
  min_key = np.min(train_data)
  max_key = np.max(train_data)
  train_data = (train_data - min_key) / (max_key - min_key)
  validating_data = (validating_data - min_key) / (max_key - min_key)
  
  train_label = (train_label - min_key) / (max_key - min_key)
  validating_label = (validating_label - min_key) / (max_key - min_key)
  
  model = keras.models.Sequential([
    keras.Input(shape=(data_size,)),
    Dense(300, activation='elu', name="Hidden_Layer_1"),
    BatchNormalization(),
    Dropout(0.2),
    Dense(200, activation='elu', name="Hidden_Layer_2"),
    BatchNormalization(),
    Dropout(0.2),
    Dense(100, activation='elu', name="Hidden_Layer_3"),
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
    batch_size=1000,
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

def model_predict(user_data):
  global model
  
  prediction = model.predict(user_data)
  return np.argmax(prediction, axis=1)

  
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

# user_list[0][0] = index
# user_list[0][1] = age
# user_list[0][2] = member_type
product_name = {
  
}
  
if model is None:
  model_train()
else:

  input_data = "4인 가족이 사용할 제품을 추천해주세요. 나이는 30대 중반입니다. 렌탈료는 3만원 정도가 좋겠어요."
  # 예시 문장 집합 (실제 사용시 제품 설명, 사용자 유형 등과 연결 필요)
  columns = ['나이', '가족 구성원', '렌탈비용', '용량', '만족도', '제품색깔', '할인율', '제품코드']
  # 가족 구성원 정보 추출 및 매칭 함수 (cosine 유사도 기반)
  def extract_member_type(text):
    candidates = list(member_type_reverse.keys())
    vectorizer = TfidfVectorizer().fit(candidates + [text])
    text_vec = vectorizer.transform([text])
    candidate_vecs = vectorizer.transform(candidates)
    similarities = cosine_similarity(text_vec, candidate_vecs)[0]
    best_idx = np.argmax(similarities)
    # 유사도가 0.2 이상일 때만 매칭 (임계값 조정 가능)
    if similarities[best_idx] > 0.2:
      return member_type_reverse[candidates[best_idx]]
    return None

  member_type_value = extract_member_type(input_data)

  vectorizer = TfidfVectorizer(vocabulary=columns)
  input_tokens = [col for col in columns if col in input_data]
  input_sentence = ' '.join(input_tokens)
  user_data = vectorizer.transform([input_sentence]).toarray()
  user_data[1] = member_type_value
  # 가장 유사한 문장의 인덱스를 기반으로 user_data 생성 (예시)
  pred_idx = model_predict(user_data)
  print("predict product : ", product_name[pred_idx])
  
  
  