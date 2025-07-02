from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session
import boto3 
from botocore.config import Config
import json
import sqlite3

# -------------------------------------------------------------------------------------
# aws key setting
access_key = ''
secret_key = ''
knowledge_base_id1 = ''
region_name =''
llm_model = ''
model_arn = ''

try:
    with open('../access_key.json', 'r') as f:
        keys = json.load(f)
        access_key = keys.get('access_key', '')
        secret_key = keys.get('secret_key', '')
        knowledge_base_id1 = keys.get('knowledge_base_id1', '')
        region_name =keys.get('region_name', '')
        llm_model = keys.get('llm_model', '')
        model_arn = keys.get('model_arn', '')
    if not access_key or not secret_key:
        raise ValueError("Access key or secret key is missing in access_key.json")

except FileNotFoundError:
    raise FileNotFoundError("access_key.json 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except json.JSONDecodeError:
    raise ValueError("access_key.json 파일의 형식이 잘못되었습니다. JSON 형식을 확인하세요.")
# -------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# AWS Bedrock 모델 초기화
# boto3를 사용하여 AWS Bedrock 모델(anthropic.claude-3-5-haiku)에 접근합니다.
# init_boto3_client 함수로 Bedrock 클라이언트를 초기화하고, converse_with_bedrock 함수로 모델과 대화합니다.
def init_boto3_client(region: str):
    if not access_key or not secret_key:
        raise ValueError("AWS 자격 증명이 설정되지 않았습니다.")

    retry_config = Config(
        region_name=region,
        retries={"max_attempts": 10, "mode": "standard"}
    )
    return boto3.client(
        # service_name="bedrock-runtime",
        service_name="bedrock-agent-runtime",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        config=retry_config
    )
# --------------------------------------------------------------------------------------
# USE KNOWLEDGE_BASE
# --------------------------------------------------------------------------------------
# AWS 베드락 지식기반 연결 : 자연어 => SQL 변경 
def converse_with_bedrock_kb(boto3_client, sys_prompt, usr_prompt):    
    temperature = 0.0
    top_p = 0.1
    inference_config = {"temperature": temperature, "topP": top_p}
    response = boto3_client.retrieve_and_generate(
    input= {"text": sys_prompt[0]["text"] + user_prompt[0]["content"][0]["text"]+ "\nSkip the preamble and provide only the SQL."},
     retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",  
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": knowledge_base_id1, # 지식기반 woongdalsam 
            "modelArn": model_arn, 
        }
    }
)
    return response['output']

# AWS 베드락 지식기반 연결 : SQL => 자연어
def natural_answer_from_result_with_kb(boto3_client, prompt_text: str):
    response = boto3_client.retrieve_and_generate(
        input={"text": prompt_text},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": knowledge_base_id1,
                "modelArn": model_arn,
            }
        }
    )
    return response["output"]["text"]
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# bedrock LLM 통신 함수 
def converse_with_bedrock(boto3_client, sys_prompt, usr_prompt):    
    temperature = 0.0
    top_p = 0.1
    inference_config = {"temperature": temperature, "topP": top_p}
    
    response = boto3_client.converse(
        modelId=llm_model, 
        messages=usr_prompt, 
        system=sys_prompt,
        inferenceConfig=inference_config
    )

    return response['output']['message']['content'][0]['text']
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# bedrock client 가져오기 
boto3_client = init_boto3_client(region_name)
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# 데이터베이스의 테이블 및 컬럼 정보를 가져와 SQL 쿼리 생성을 위한 스키마 정보를 출력합니다.
def get_schema_info(db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    inspector = inspect(engine)
    schema_info = {}
    tables = inspector.get_table_names()
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        table_info = f"Table: {table_name}\n" + "\n".join(f"  - {col['name']} ({col['type']})" for col in columns)
        schema_info[table_name] = table_info
    return schema_info

schema = get_schema_info("aiChallenge.db")
# -------------------------------------------------------------------------------------
# PROMPT
# -------------------------------------------------------------------------------------
# SYSTEM PROMPT 
dialect = "sqlite"
top_k = 10
table_info = schema['customer'] # 테이블 정보를 다 가져왔으므로~ 

sys_prompt = [{
    "text": f"""You are a {dialect} expert.
Given an input question, first create a syntactically correct SQLite query to run. 
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date(\'now\') function to get the current date, if the question involves "today" 

Guidelines:
- If values like age are vague (e.g., "mid-30s"), estimate them (e.g., 35).
- If values are missing, use 0 for numbers and "" for text values.
- If the input describes a condition or query, generate a `SELECT` statement.
- If the input describes new data, generate an `INSERT` statement.
- Output only the SQL query. No explanations, comments, or formatting.
- Use standard SQLite syntax.

Only use the following tables:
{table_info}
""" 
}]

# 유저 프롬프트 return하는 함수 
def get_user_prompt(question):
    return [{
        "role": "user",
        "content": [{"text": f"Question:\n{question}]\n\n  Skip the preamble and provide only the SQL" #서문 건너뛰고 sql만 제공
        }]
    }]


# sql => 자연어 prompt
def sqlToText_prompt(sql_query: str, result) -> str:
    if not result:
        return "쿼리 결과가 없습니다."

    return f"""
                SQL 쿼리:
                {sql_query}

                결과:
                {result}

                위 쿼리와 결과에 대한 자연어 설명을 해줘. 
                예를 들어, 평균 나이가 51.5세이면 "정수기 사용자의 평균 나이는 51.5세에요." 와 같은 식으로 대답해줘.
                """


# -------------------------------------------------------------------------------------
# 사용자 상호작용 
question = input("❓질문을 입력하세요.\n")
user_prompt = get_user_prompt(question)

response = converse_with_bedrock_kb(boto3_client, sys_prompt, user_prompt)
sql_query = response['text']
print("🤖쿼리로 알려드릴게요.....")
print(sql_query)

# -------------------------------------------------------------------------------------
# 사용자가 입력한 쿼리를 DB에서 실행 후 결과 반환 
conn = sqlite3.connect("aiChallenge.db")
cur = conn.cursor()

result = cur.execute(sql_query).fetchall()
print("SQL Query Result:"+str(result))

# sql_query,result 을 기반으로 자연어 응답 생성
# 1.get sqlToText prompt
prompt_text = sqlToText_prompt(sql_query, result)
# 2.자연어 prompt & 지식기반 활용하여 응답값 반환
natural_answer = natural_answer_from_result_with_kb(boto3_client, prompt_text)
print("🤖결과를 알려드릴게요.....")
print(natural_answer)