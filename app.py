from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # CSV 파일 읽기 등 모든 복잡한 기능을 제거하고,
    # 오직 이 문장만 화면에 보여주는 테스트용 코드입니다.
    return "<h1>서버가 정상적으로 작동합니다.</h1> <p>이 화면이 보이면, 배포의 기본 설정은 성공한 것입니다.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)