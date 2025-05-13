import requests
from bs4 import BeautifulSoup
import json

def get_lecture_data(user_id: str, password: str):
    # 시텔 KLAS 객\uxc778 계\uxc815 검사가 안 되는 경우, 또는 테스트에서 통신만 하고 싶을 때 사용
    return {
        "lectureName": "AIÆ구문",
        "startDate": "2025-05-10 00:00",
        "endDate": "2025-05-20 23:59"
    }

    # 테스트가 안인 경우가 아니면, 이전의 실천 사용을 보게

    session = requests.Session()

    # 1. 로그인 요청
    login_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginConfirm.do"
    login_data = {
        "loginId": user_id,
        "passwd": password,
    }
    login_res = session.post(login_url, data=login_data)

    if login_res.status_code != 200 or "LoginFail" in login_res.text:
        return {"error": "로그인 실패"}

    # 2. 일정 정보 요청
    schedule_url = "https://klas.kw.ac.kr/std/cmn/frame/SchdulStList.do"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    schedule_res = session.post(schedule_url, headers=headers)

    if schedule_res.status_code != 200:
        return {"error": "일정 정보 요청 실패"}

    try:
        data = schedule_res.json()
        for item in data.get("list", []):
            if item.get("typeNm") == "과제":
                return {
                    "lectureName": item.get("schdulTitle", ""),
                    "startDate": parse_time(item.get("started")),
                    "endDate": parse_time(item.get("ended"))
                }

        return {"error": "오류나인 경우의 일정이 없음"}
    except Exception as e:
        return {"error": f"JSON 파싱 실패: {str(e)}"}

def parse_time(klas_str):
    if not klas_str or len(klas_str) < 12:
        return ""
    return f"{klas_str[0:4]}-{klas_str[4:6]}-{klas_str[6:8]} {klas_str[8:10]}:{klas_str[10:12]}"
