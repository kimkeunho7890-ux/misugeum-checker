import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CSV 파일을 읽어서 데이터프레임으로 저장
# 서버 환경 호환성을 위해 파일 이름을 영어로 바꾸고, 인코딩을 utf-8로 변경
try:
    df = pd.read_csv('data.csv', encoding='utf-8')
    # 숫자처럼 보이는 POS코드를 문자로 취급하여 오류 방지
    df['코드'] = df['코드'].astype(str)
except FileNotFoundError:
    print("'data.csv' 파일을 찾을 수 없습니다. 같은 폴더에 파일이 있는지 확인하세요.")
    df = None
except Exception as e:
    print(f"파일을 읽는 중 오류 발생: {e}")
    df = None


@app.route('/')
def index():
    """첫 접속 시 보여줄 메인 페이지를 렌더링합니다."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """POS코드를 받아 모든 정산 내역 리스트를 찾아주는 함수입니다."""
    if df is None:
        return jsonify({"error": "데이터 파일을 불러오지 못했습니다."}), 500
        
    user_pos_code = request.json.get('code')
    
    # POS코드로 해당되는 모든 행을 찾습니다.
    result_df = df[df['코드'] == user_pos_code]
    
    if not result_df.empty:
        # 판매점명은 첫 번째 행에서 가져옵니다.
        store_name = result_df.iloc[0]['판매처']
        
        # 필요한 컬럼들만 선택하여 리스트 형태로 변환합니다.
        transactions = result_df[['정산년월', '정산항목', '상세내용', '정산금액']].to_dict('records')
        
        # 필요한 정보를 JSON 형태로 가공하여 프론트엔드로 보냅니다.
        response_data = {
            "store_name": store_name,
            "transactions": transactions
        }
        return jsonify(response_data)
    else:
        # 검색 결과가 없을 경우 에러 메시지를 보냅니다.
        return jsonify({"error": "해당 POS코드를 찾을 수 없습니다."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)