import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    if os.path.exists(path):
        models['rf'] = joblib.load(path)
    return models

models = load_models()

# --- 2. GIAO DIỆN NHẬP LIỆU (HTML) ---
html_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; padding: 10px; }
        .card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
        label { font-size: 10px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-left: 5px; }
        input { border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; margin-bottom: 12px; outline: none; background: #f8fafc; }
        input:focus { border-color: #10b981; background: white; }
        button { background: #059669; color: white; width: 100%; padding: 15px; border-radius: 15px; font-weight: bold; cursor: pointer; transition: 0.2s; border: none; shadow: 0 4px 6px rgba(5, 150, 105, 0.2); }
        button:hover { background: #047857; transform: translateY(-1px); }
    </script>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <h2 style="text-align:center; color:#1e293b; margin-bottom: 20px; font-weight: 800;">AgroPredict <span style="color:#10b981;">AI</span></h2>
        <div style="grid-template-columns: 1fr 1fr; display: grid; gap: 10px;">
            <div><label>Nitơ (N)</label><input id="n" type="number" value="14"></div>
            <div><label>Phốt pho (P)</label><input id="p" type="number" value="52"></div>
        </div>
        <label>Kali (K)</label><input id="k" type="number" value="76">
        <div style="grid-template-columns: 1fr 1fr; display: grid; gap: 10px;">
            <div><label>Nhiệt độ (°C)</label><input id="temp" type="number" value="28"></div>
            <div><label>Lượng mưa (mm)</label><input id="rain" type="number" value="250"></div>
        </div>
        <button onclick="send()">DỰ ĐOÁN NGAY →</button>
    </div>
    <script>
        function send() {
            const data = {
                n: document.getElementById('n').value,
                p: document.getElementById('p').value,
                k: document.getElementById('k').value,
                temp: document.getElementById('temp').value,
                rain: document.getElementById('rain').value
            };
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(data)}, '*');
        }
    </script>
</body>
</html>
'''

# Hiển thị Form nhập liệu
data_input = components.html(html_form, height=520)

# Tạo một vùng trống để hiển thị kết quả
result_container = st.empty()

# --- 3. XỬ LÝ DỰ ĐOÁN VÀ HIỂN THỊ ---
if data_input:
    try:
        # Giải mã dữ liệu
        d = json.loads(data_input)
        
        # Chuẩn bị DataFrame (Lưu ý: Tên cột phải giống hệt lúc Train Model)
        df = pd.DataFrame([[
            float(d['n']), float(d['p']), float(d['k']), 
            float(d['temp']), float(d['rain'])
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if 'rf' in models:
            # Chạy Model dự đoán
            res = models['rf'].predict(df)[0]
            
            # Giao diện hiển thị kết quả Dark Mode
            res_html = '''
            <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); 
                        padding: 40px; border-radius: 30px; color: white; text-align: center; 
                        margin: 20px auto; max-width: 450px; border: 1px solid #10b981;
                        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);">
                <p style="color: #10b981; font-weight: 900; font-size: 12px; text-transform: uppercase; letter-spacing: 2px;">Phân tích thành công</p>
                <h3 style="color: #94a3b8; font-size: 11px; margin-top: 20px; text-transform: uppercase;">Năng suất ước tính</h3>
                <h2 style="font-size: 48px; font-weight: 800; margin: 10px 0; color: #ffffff;">
                    {:.3f} <span style="font-size: 16px; color: #64748b; font-weight: 400;">tấn/ha</span>
                </h2>
                <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 20px auto; width: 60%;"></div>
                <p style="font-size: 10px; color: #475569;">Mô hình: Random Forest Regressor</p>
            </div>
            '''.format(res)
            
            # Đổ kết quả vào vùng trống đã tạo
            result_container.markdown(res_html, unsafe_allow_html=True)
            st.balloons()
        else:
            result_container.error("⚠️ Không tìm thấy tệp model (.pkl) trong thư mục backend/model/")

    except Exception as e:
        result_container.error(f"❌ Lỗi xử lý: {e}")
else:
    result_container.info("💡 Điền thông số và nhấn nút để xem kết quả phân tích.")
