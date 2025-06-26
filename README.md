# ai-challenge

필수 라이브러리 설치

```
python version 3.9.0
pip version(latest, 25.1.1)

모델 학습에 필요한 라이브러리
pip install tensorflow (2.5.0)
pip install keras
pip install pandas (2.3)

그래프 시각화 도구
pip install matplotlib

배열 연산을 쉽게 해주는 라이브러리
pip install numpy (1.23)

AWS Bedrock 연결에 필요한 라이브러리
pip install boto3
```

## 어플리케이션 주요 기능
고객별 제품 추천 챗봇, 고객이 직접 봇과 채팅하며 제품을 추천받음

## Architecture Concept

![concept](https://github.com/user-attachments/assets/2e246de1-f22a-478b-b8ec-5b57f837b328)

```
사용자의 제품 구매 데이터를 학습한 모델을 만들어 저장한다.

질문자가 query를 던지면 AWS Bedrock에 등록된 프롬프트가 이를 해석해 모델에 들어가는 shape에 맞춰 벡터화한다.

변환된 vector data를 모델에 input 하면 추천 제품의 결과를 추천해준다.
```



## training model information

```
data size : 70,000
train data size : 63,000
validating data size : 7,000
input shape : (6, )

Hidden Layer 1 : 6 by 30, activation function : ELU
Hidden Layer 2 : 30 by 15, activation function : ELU
Output Layer 3 : 15 by 10, activation function : softmax

epoch = 100
batch size = 5000

```

초기 세팅 시 epoch가 60에서 더이상 진전이 없다.

![train history](https://github.com/user-attachments/assets/f876ec55-b13d-4cb5-b102-dc518d7c295b)

해당 모델이 잘 만들어졌는지 단위 테스트 해 보았다.

![pic 3](https://github.com/user-attachments/assets/96779534-06b3-4be9-b524-206ae54e3df9)


간단한 데이터셋으로 훈련시켰지만 어느정도 예측에 성공하였습니다.

## AWS Bedrock 세팅




