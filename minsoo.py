import sqlite3
import boto3
from botocore.config import Config


# DB 연결 (없으면 생성됨)
conn = sqlite3.connect("aiChallenge.db")
cur = conn.cursor()


cur.execute(
'''
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY,
    age INTEGER,
    houseHold INTEGER,
    amt INTEGER,
    size INTEGER,
    score INTEGER,
    discRate INTEGER,
    prdtGrpCd TEXT,
    prdtCd TEXT
);

'''
)


cur.execute(
'''INSERT INTO customer (
    age, houseHold, amt, size, score, discRate, prdtGrpCd, prdtCd
) VALUES (
    35, 4, 30, 30, 75, 10, '정수기', '정수기1'
)''')

result = cur.execute(
    '''select * from customer'''
).fetchall()


# # 1. 인증 정보 로드
# with open('access_key.json', 'r') as f:
#     keys = json.load(f)
#     access_key = keys.get('access_key', '')
#     secret_key = keys.get('secret_key', '')

# # 2. 클라이언트 생성
# client = boto3.client(
#     service_name='bedrock-agent-runtime',
#     region_name='ap-northeast-2',  # 사용 중인 리전에 맞게 수정
#     aws_access_key_id=access_key,
#     aws_secret_access_key=secret_key
# )

# # 3. 필수 값
# knowledge_base_id = 'WYZTUXIVXS'



# def query_llm(natural_text):
#     # Bedrock - Claude 호출 (가상 함수)
#     return generate_sql_from_prompt(natural_text)

# def execute_sql(sql):
#     conn = sqlite3.connect('orders.db')
#     cur = conn.cursor()
#     cur.execute(sql)
#     result = cur.fetchall()
#     conn.close()
#     return result

# question = "20대 여성이 가장 많이 산 식기세척기를 알려줘"
# sql = query_llm(question)
# result = execute_sql(sql)

# print("질문:", question)
# print("생성된 SQL:", sql)
print("결과:", result)

conn.commit()
conn.close()