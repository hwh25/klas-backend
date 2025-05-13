from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from klas_scraper import get_lecture_data  # 👈 스크래핑 함수 불러오기

app = FastAPI()

# 사용자 로그인 정보를 저장하는 임시 메모리 저장소
user_accounts: Dict[str, str] = {}

# 로그인 요청에 사용할 데이터 모델
class LoginRequest(BaseModel):
    user_id: str
    password: str

# 로그인 정보를 저장하는 POST API
@app.post("/login")
def save_login(data: LoginRequest):
    user_accounts[data.user_id] = data.password
    return {"message": "저장됨"}

# 사용자 ID로 강의 정보를 가져오는 GET API
@app.get("/klas/{user_id}")
def get_info(user_id: str):
    if user_id not in user_accounts:
        return {"error": "등록되지 않은 사용자입니다"}

    password = user_accounts[user_id]
    return get_lecture_data(user_id, password)
