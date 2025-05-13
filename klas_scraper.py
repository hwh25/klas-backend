import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_lecture_data(user_id: str, password: str):
    session = requests.Session()

    # 1. 로그인
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
        now = datetime.now()
        data = schedule_res.json()

        for item in data.get("list", []):
            if item.get("typeNm") == "과제":
                end_str = item.get("ended", "")
                end_time = datetime.strptime(end_str, "%Y%m%d%H%M%S")
                if end_time > now:
                    return {
                        "lectureName": item.get("schdulTitle", ""),
                        "startDate": parse_time(item.get("started")),
                        "endDate": parse_time(item.get("ended"))
                    }

        return {"error": "예정된 강의 일정 없음"}

    except Exception as e:
        return {"error": f"JSON 파싱 실패: {str(e)}"}

def parse_time(klas_str):
    if not klas_str or len(klas_str) < 12:
        return ""
    return f"{klas_str[0:4]}-{klas_str[4:6]}-{klas_str[6:8]} {klas_str[8:10]}:{klas_str[10:12]}"
