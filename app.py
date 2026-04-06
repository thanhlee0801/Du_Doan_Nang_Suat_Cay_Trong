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
    # Đảm bảo tên file này chính xác với file trong Repo của bạn
    files = {'rf': 'random_forest_model.pkl'} 
    for key, name in files.items():
        path = os.path.join(MODEL_DIR, name)
        if os.path.exists(path):
            models[key] = joblib.load(path)
    return models

models = load_models()

# --- 2. GIAO DIỆN HTML & CSS ---
html_code = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; padding: 20px; }
        .card { background: white; border-radius: 24px; padding: 24px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
        input { border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; margin-bottom: 12px; outline: none; }
        input:focus { border-color: #10b981; }
        button { background: #10b981; color: white; font-weight: bold; padding: 12px; width: 100%; border-radius: 12px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #059669; }
    </style>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <h2 class="text-2xl font-bold text-emerald-800 mb-6 text-center">Nông Nghiệp AI</h2>
        <label style="font-size: 12px; font-weight: bold; color: #64748b;">NITƠ (N)</label>
        <input id="n" type="number" value="14">
        <label style="font-size: 12px; font-weight: bold; color: #64748b;">PHỐT PHO (P)</label>
        <input id="p" type="number" value="52">
        <label style="font-size: 12px; font-weight: bold; color: #64748b;">KALI (K)</label>
        <input id="k" type="number" value="76">
        <label style="font-size: 12px; font-weight: bold; color: #64748b;">NHIỆT ĐỘ (°C)</label>
        <input id="temp" type="number" value="28">
        <label style="font-size: 12px; font-weight: bold; color: #64748b;">LƯỢNG MƯA (mm)</label>
        <input id="rain" type="number" value="250">
        <button onclick="sendData()">DỰ ĐOÁN NGAY</button>
    </div>

    <script>
        function sendData() {
            const payload = {
                n: parseFloat(document.getElementById('n').value),
                p: parseFloat(document.getElementById('p').value),
                k: parseFloat(document.getElementById('k').value),
                temp: parseFloat(document.getElementById('temp').value),
                rain: parseFloat(document.getElementById('rain').value)
            };
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify(payload)
            }, '*');
        }
    </script>
</body>
</html>
'''

# Hiển thị giao diện HTML
data_input = components.html(html_code, height=550)

# --- 3. XỬ LÝ DỰ ĐOÁN ---
if data_input:
    try:
        # Giải mã JSON từ HTML gửi về
        clean_dict = json.loads(data_input)
        
        # Tạo DataFrame (Kiểm tra kỹ tên cột N, P, K, temperature, rainfall)
        df = pd.DataFrame([[
            clean_dict['n'], clean_dict['p'], clean_dict['k'], 
            clean_dict['temp'], clean_dict['rain']
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if 'rf' in models:
            res = models['rf'].predict(df)[0]
            
            # Hiển thị kết quả bằng Markdown với style Dark Mode
            st.markdown(f'''
                <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); 
                            padding: 30px; border-radius: 20px; color: white; text-align: center; margin-top: 20px;">
                    <p style="color: #10b981; font-weight: bold; text-transform: uppercase; font-size: 12px; margin: 0;">Kết quả dự đoán</p>
                    <h2 style="font-size: 42px; margin: 15px 0;">{res:.3f} <span style="font-size: 16px; color: #94a3b8;">tấn/ha</span></h2>
                    <p style="font-size: 11px; color: #64748b;">Dựa trên dữ liệu môi trường và dinh dưỡng đất</p>
                </div>
            ''', unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("⚠️ Không tìm thấy file model (random_forest_model.pkl)")

    except Exception as e:
        st.error(f"❌ Lỗi: {str(e)}")
else:
    st.info("💡 Nhập thông số và nhấn 'DỰ ĐOÁN NGAY' để xem kết quả.")
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
