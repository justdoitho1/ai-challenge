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


## concept

![concept](https://github.com/user-attachments/assets/2e246de1-f22a-478b-b8ec-5b57f837b328)

```
사용자의 제품 구매 데이터를 학습한 모델을 만들어 저장한다.

질문자가 query를 던지면 AWS Bedrock에 등록된 프롬프트가 이를 해석해 모델에 들어가는 shape에 맞춰 벡터화한다.

변환된 vector data를 모델에 input 하면 추천 제품의 결과를 추천해준다.
```
