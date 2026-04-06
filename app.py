import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
MODEL_PATH = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/random_forest_model.pkl"

# Load model (Backend)
@st.cache_resource
def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

model = get_model()

# --- GIAO DIỆN HTML (PHẢI CÓ JS ĐÚNG) ---
html_code = """
<script>
    function gui_du_lieu() {
        const data = {
            n: parseFloat(document.getElementById('n').value),
            p: parseFloat(document.getElementById('p').value),
            k: parseFloat(document.getElementById('k').value),
            temp: parseFloat(document.getElementById('temp').value),
            rain: parseFloat(document.getElementById('rain').value)
        };
        // Lệnh quan trọng nhất để Streamlit nhận được data
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: data
        }, '*');
    }
</script>
<div style="background: white; p: 20px; border-radius: 20px;">
    <input id="n" type="number" placeholder="N">
    <input id="p" type="number" placeholder="P">
    <input id="k" type="number" placeholder="K">
    <input id="temp" type="number" placeholder="Nhiệt độ">
    <input id="rain" type="number" placeholder="Lượng mưa">
    <button onclick="gui_du_lieu()">DỰ ĐOÁN NGAY</button>
</div>
"""

# Hiển thị và hứng dữ liệu
# CHÚ Ý: Biến 'data_output' sẽ chứa dữ liệu khi bạn nhấn nút DỰ ĐOÁN
data_output = components.html(html_code, height=400)

# --- XỬ LÝ DỰ ĐOÁN ---
if data_output is not None:
    # 1. Chuyển dữ liệu sang DataFrame
    input_df = pd.DataFrame([data_output])
    # Đổi tên cột cho khớp với model (Ví dụ: n -> N)
    input_df.columns = ['n', 'p', 'k', 'temp', 'rain'] 
    
    if model:
        # 2. Dự đoán
        prediction = model.predict(input_df)[0]
        
        # 3. Hiển thị (Đây là phần bạn đang bị thiếu)
        st.write("---")
        st.success(f"### Kết quả dự đoán: {prediction:.2f} tấn/ha")
        st.balloons()
    else:
        st.error("Không tìm thấy model để dự đoán!")
