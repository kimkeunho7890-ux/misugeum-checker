import pandas as pd
from flask import Flask, render_template, request, jsonify
import traceback # 에러 상세 출력을 위한 라이브러리

app = Flask(__name__)

# --- 데이터 로딩 부분 ---
df = None
initial_error = None

try:
    # 서버 환경에서 파일을 확실히 읽기 위해 인코딩 옵션을 추가합니다.
    df = pd.read_csv('data.csv', encoding='utf-8-sig') 
    df['코드'] = df['코드'].astype(str)
    print("CSV file loaded successfully.")
except FileNotFoundError:
    initial_error = "CRITICAL ERROR: 'data.csv' 파일을 찾을 수 없습니다. GitHub에 파일이 제대로 업로드되었는지 확인하세요."
    print(initial_error)
except Exception as e:
    # 앱이 멈추게 하는 모든 오류를 잡아서 상세히 출력합니다.
    tb_str = traceback.format_exc()
    initial_error = f"CRITICAL ERROR: CSV 파일을 읽는 중 심각한 오류 발생.\n{e}\n\n{tb_str}"
    print(initial_error)
# --- 데이터 로딩 끝 ---


@app.route('/')
def index():
    """첫 접속 시 보여줄 메인 페이지를 렌더링합니다."""
    # 앱 시작 시 오류가 있었다면, 그 오류를 화면에 표시합니다.
    if initial_error:
        return f"<pre>{initial_error}</pre>", 500
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """POS코드를 받아 모든 정산 내역 리스트를 찾아주는 함수입니다."""
    if df is None:
        return jsonify({"error": initial_error or "데이터 파일을 불러오지 못했습니다."}), 500
        
    user_pos_code = request.json.get('code')
    result_df = df[df['코드'] == user_pos_code]
    
    if not result_df.empty:
        store_name = result_df.iloc[0]['판매처']
        transactions = result_df[['정산년월', '정산항목', '상세내용', '정산금액']].to_dict('records')
        response_data = { "store_name": store_name, "transactions": transactions }
        return jsonify(response_data)
    else:
        return jsonify({"error": "해당 POS코드를 찾을 수 없습니다."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)