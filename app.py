import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Đường dẫn tới thư mục model
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    files = {'rf': 'random_forest_model.pkl'} # Thêm các model khác vào đây nếu có
    for key, name in files.items():
        path = os.path.join(MODEL_DIR, name)
        if os.path.exists(path):
            models[key] = joblib.load(path)
    return models

models = load_models()

# --- 2. GIAO DIỆN HTML & CSS ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; padding: 20px; }
        .card { background: white; border-radius: 24px; padding: 24px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
        input { border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <h2 class="text-2xl font-bold text-emerald-800 mb-4 text-center">AgroPredict AI</h2>
        <input id="n" type="number" placeholder="Nitơ (N)" value="14">
        <input id="p" type="number" placeholder="Phốt pho (P)" value="52">
        <input id="k" type="number" placeholder="Kali (K)" value="76">
        <input id="temp" type="number" placeholder="Nhiệt độ (°C)" value="28">
        <input id="rain" type="number" placeholder="Lượng mưa (mm)" value="250">
        <button onclick="predict()" class="w-full bg-emerald-600 text-white font-bold py-3 rounded-xl shadow-lg mt-2">DỰ ĐOÁN NGAY</button>
    </div>

    <script>
        function predict() {
            const payload = {
                n: parseFloat(document.getElementById('n').value) || 0,
                p: parseFloat(document.getElementById('p').value) || 0,
                k: parseFloat(document.getElementById('k').value) || 0,
                temp: parseFloat(document.getElementById('temp').value) || 0,
                rain: parseFloat(document.getElementById('rain').value) || 0
            };
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify(payload)
            }, '*');
        }
    </script>
</body>
</html>
"""

# Hiển thị giao diện
data_input = components.html(html_code, height=500)

# --- 3. XỬ LÝ DỰ ĐOÁN ---
if data_input:
    try:
        # Giải mã an toàn để tránh lỗi .keys()
        clean_dict = json.loads(data_input)
        
        # Tạo DataFrame (Tên cột phải khớp chính xác với Model của bạn)
        df = pd.DataFrame([[
            clean_dict['n'], clean_dict['p'], clean_dict['k'], 
            clean_dict['temp'], clean_dict['rain']
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if models and 'rf' in models:
            res = models['rf'].predict(df)[0]
            
            # Hiển thị kết quả bằng Markdown HTML
            st.markdown(f'''
                <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-top: 20px;">
                    <p style="color: #10b981; font-weight: bold; text-transform: uppercase; font-size: 12px;">Dự đoán thành công</p>
                    <h2 style="font-size: 32px; margin: 10px 0;">{res:.3f} <small style="font-size: 14px; color: #94a3b8;">tấn/ha</small></h2>
                </div>
            ''', unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Không tìm thấy model (.pkl)")

    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")

# --- 4. HIỂN THỊ KẾT QUẢ ---
if data_input:
    # Gọi hàm xử lý đã được cách ly
    ket_qua = giai_ma_va_du_doan(data_input)
    
    if isinstance(ket_qua, float):
        # Hiển thị giao diện kết quả tối màu (Dark UI)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); padding: 35px; border-radius: 24px; color: white; text-align: center; margin-top: 20px; border: 1px solid #10b981;">
            <p style="color: #10b981; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Dự đoán thành công</p>
            <h2 style="font-size: 36px; font-weight: 800; margin: 15px 0;">{ket_qua:.3f} <small style="font-size: 14px; color: #94a3b8; font-weight: 400;">tấn/ha</small></h2>
            <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 15px auto; width: 50%;"></div>
            <p style="font-size: 10px; color: #64748b;">Mô hình: Random Forest Regressor</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.error(f"Hệ thống báo lỗi: {ket_qua}")
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.error(f"Hệ thống chưa thể phân tích: {ket_qua}")
