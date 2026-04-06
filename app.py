import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import json

# 1. Load Model
@st.cache_resource
def load_model():
    # Điều chỉnh đường dẫn này cho đúng với file của bạn trên GitHub
    path = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/random_forest_model.pkl"
    return joblib.load(path)

try:
    model = load_model()
except:
    st.error("Chưa tìm thấy file model.pkl!")

# 2. Khởi tạo giá trị ban đầu là 0
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = 0.0

# 3. Giao diện nhập liệu siêu đơn giản (Để test nút bấm)
html_input = '''
    <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #ccc;">
        <input id="n" type="number" value="14" placeholder="N">
        <input id="p" type="number" value="52" placeholder="P">
        <input id="k" type="number" value="76" placeholder="K">
        <input id="temp" type="number" value="28" placeholder="Temp">
        <input id="rain" type="number" value="250" placeholder="Rain">
        <button onclick="gui_du_lieu()">DỰ ĐOÁN NGAY</button>
    </div>
    <script>
        function gui_du_lieu() {
            const d = {
                n: document.getElementById('n').value,
                p: document.getElementById('p').value,
                k: document.getElementById('k').value,
                temp: document.getElementById('temp').value,
                rain: document.getElementById('rain').value
            };
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(d)}, '*');
        }
    </script>
'''

# Hiển thị form và nhận dữ liệu
data_from_js = components.html(html_input, height=200)

# 4. Xử lý khi nhấn nút (Dữ liệu trả về từ JS)
if data_from_js and isinstance(data_from_js, str):
    payload = json.loads(data_from_js)
    # Chuyển thành DataFrame
    df = pd.DataFrame([[
        float(payload['n']), float(payload['p']), float(payload['k']), 
        float(payload['temp']), float(payload['rain'])
    ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])
    
    # Dự đoán và cập nhật session_state
    st.session_state.ket_qua = model.predict(df)[0]
    st.rerun()

# 5. Hiển thị kết quả (Dạng thô trước để kiểm tra)
st.write(f"### Kết quả hiện tại: {st.session_state.ket_qua:.3f} tấn/ha")
