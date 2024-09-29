from flask import Flask, render_template, request, redirect, make_response
import json
import os

app = Flask(__name__)

# JSON 파일 경로
DATA_FILE = 'data.json'

# 데이터 로드 함수
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}  # 파일이 없으면 빈 딕셔너리 반환
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)  # JSON 파일 읽기
    except (json.JSONDecodeError, ValueError):  # JSONDecodeError 또는 잘못된 형식 처리
        return {}  # 오류 발생 시 빈 딕셔너리 반환

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 홈 페이지 - 이름 입력 폼
@app.route('/', methods=['GET', 'POST'])
def index():
    # 이미 이름을 입력한 경우 쿠키 체크
    # if request.cookies.get('already_submitted'):
    #     # 데이터 로드
    #     data = load_data()
    #     # 이미 입력한 경우, 입력 불가 페이지로 이동
    #     return render_template('already_submitted.html', names=data)

    if request.method == 'POST':
        name = request.form['name']
        if name:
            # 데이터 로드
            data = load_data()
            
            # 이름이 이미 있으면 횟수를 증가시키고, 없으면 1로 설정
            if name in data:
                data[name] += 1
            else:
                data[name] = 1
            
            # 데이터 저장
            save_data(data)

            # 쿠키에 'already_submitted' 설정 (만료 기간은 1년으로 설정)
            response = make_response(redirect('/'))
            response.set_cookie('already_submitted', 'true', max_age=60*60*24*365)  # 1년 동안 유효
            return response

    # 저장된 이름 목록 가져오기
    data = load_data()
    return render_template('index.html', names=data)

if __name__ == '__main__':
    app.run(debug=True)
