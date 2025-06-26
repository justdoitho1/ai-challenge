# ai-challenge


## 개발 환경
python version 3.9.0

### Dependency
```
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
사용자의 제품 구매 데이터를 학습한 모델을 만들어 저장합니다.

질문자가 query를 던지면 AWS Bedrock에 등록된 프롬프트가 이를 해석해 모델에 들어가는 shape에 맞춰 벡터화합니다.

변환된 vector data를 모델에 input 하면 추천 제품의 결과를 추천해줍니다.
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

초기 훈련 시 epoch를 100으로 하여 훈련했는데 epoch가 60에서 더이상 진전이 없습니다.
정확도 또한 epoch 60부터 1에 근접한 값으로 수렴하고 있습니다.

![train history](https://github.com/user-attachments/assets/f876ec55-b13d-4cb5-b102-dc518d7c295b)

해당 모델이 잘 만들어졌는지 단위 테스트 해 보았습니다.

![pic 3](https://github.com/user-attachments/assets/96779534-06b3-4be9-b524-206ae54e3df9)


간단한 데이터셋으로 훈련시켰지만 어느정도 예측에 성공하였습니다.

## AWS Bedrock 세팅

먼저 발급받은 계정을 백엔드 서버에서 접근할 수 있도록 access key를 발급받습니다

![pic 4](https://github.com/user-attachments/assets/eb543408-c568-47b4-893d-e8bff7de8faa)

![pic 5](https://github.com/user-attachments/assets/4e60afb0-c310-454c-8fbf-f97a83537590)

prompt 메뉴에 들어가서 새로운 prompt를 생성합니다.

![pic 6](https://github.com/user-attachments/assets/31873a4e-a246-4762-a2ee-f82af25edcb9)

prompt가 입력받을 문장을 어떻게 처리할 지 지침을 입력해줍니다.
사용자 메세지는 실제 prompt가 입력받는 데이터입니다.
prompt의 모델은 Nova Pro Model을 사용합니다.

![pic 7](https://github.com/user-attachments/assets/f5300e6a-9a25-4629-9d92-fbd7432b78b7)


생성한 prompt를 사용하려면 flow에 적용시켜야 합니다.
flow 메뉴로 들어가 신규 flow를 생성해줍니다.

![pic 8](https://github.com/user-attachments/assets/3746c2ca-3543-44b5-bdcd-6aca9aa92827)


flow builder를 편집하면 아래와 같은 다이어그램이 표시됩니다.

![pic 9](https://github.com/user-attachments/assets/323f19e1-5e77-407a-aaad-a5ec42129903)


아까 만든 prompt를 적용시킵니다.

![pic 10](https://github.com/user-attachments/assets/3b78c9fa-2598-46a0-8e4c-7ab64c550721)


테스트 결과 prompt가 메세지를 정상적으로 생성하였습니다.

![pic 11](https://github.com/user-attachments/assets/be65e9cf-8fdd-481e-bfdc-fcbcb6b6ba1b)


이 flow를 배포하려면 alias가 필요합니다.

![pic 12](https://github.com/user-attachments/assets/295ae7a5-525c-4afb-88ee-d04f4ab49fcf)


alias를 만들고 나면 prepared로 배포 준비가 완료되었고 이는 백엔드에 연결할 준비가 끝났다는 것입니다.

![pic 13](https://github.com/user-attachments/assets/bbc411f3-e19a-48e5-b60b-68f00caa8a05)


발급받은 키와 flow 연결에 필요한 id들을 관리하기 위해 json 파일에 따로 저장해 두었습니다.
이 값을 불러와 boto3 client에 적용하였습니다.

![pic 14](https://github.com/user-attachments/assets/f22dbd5a-c4b4-4e27-95c8-c57c38e57854)


문장을 입력받아 Flow에 적용하면 프롬프트의 결과가 정상 출력됩니다.

![pic 15](https://github.com/user-attachments/assets/36a48f8c-b7b4-434a-bea0-00f8450735db)


aws 연결 관련 코드는 아래 docs를 참고하였습니다.

<https://docs.aws.amazon.com/ko_kr/bedrock/latest/userguide/flows-code-ex.html>




