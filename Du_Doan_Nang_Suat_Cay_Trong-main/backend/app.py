from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route chính kiểm tra trạng thái API
@app.route('/')
def home():
    return jsonify({"message": "API Backend đang hoạt động!"})

# Route API để nhận dữ liệu từ form và dự đoán
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Tại đây, bạn sẽ tích hợp model Machine Learning của mình (ví dụ file model.pkl)
    # Tạm thời chúng ta sẽ trả về một chuỗi kết quả mẫu.
    print("Dữ liệu nhận được:", data)
    
    ket_qua = "Dự đoán mẫu: Năng suất dự kiến là 5.2 tấn/ha"
    return jsonify({'prediction': ket_qua})

if __name__ == '__main__':
    app.run(debug=True)