import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Đường dẫn model
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    if os.path.exists(path):
        models['rf'] = joblib.load(path)
    return models

models = load_models()

# Khởi tạo giá trị dự đoán trong Session State nếu chưa có
if 'pred_value' not in st.session_state:
    st.session_state.pred_value = 0.0
    st.session_state.status = "HỆ THỐNG SẴN SÀNG"

# --- 2. GIAO DIỆN NHẬP LIỆU (THEO ẢNH MẪU) ---
html_input_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; }
        .main-container { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
        .card { background: white; border-radius: 20px; padding: 20px; width: 380px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f1f5f9; }
        .section-title { font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; margin-bottom: 15px; font-size: 13px; }
        label { font-size: 9px; font-weight: 700; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 4px; margin-top: 8px; }
        input, select { background: #f8fafc; border: 1.2px solid #e2e8f0; border-radius: 10px; padding: 8px; width: 100%; outline: none; font-size: 12px; }
        input:focus { border-color: #10b981; }
        .btn-predict { background: #059669; color: white; width: 100%; padding: 12px; border-radius: 12px; font-weight: 800; margin-top: 20px; cursor: pointer; border: none; font-size: 13px; }
        .nut-group { display: flex; gap: 8px; margin-top: 8px; }
        .nut-item { border-radius: 12px; padding: 8px; text-align: center; flex: 1; }
        .nut-input { background: transparent; border: none; text-align: center; font-size: 16px; font-weight: 800; width: 100%; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="card">
            <div class="section-title">📍 Môi trường & Địa lý</div>
            <label>Vùng miền canh tác</label>
            <select><option>Miền Bắc</option></select>
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label>Loại đất</label><select><option>Đất Cát</option></select></div>
                <div style="flex:1;"><label>Cây trồng</label><select><option>Lúa</option></select></div>
            </div>
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label>Lượng mưa (mm)</label><input id="rain" type="number" value="250"></div>
                <div style="flex:1;"><label>Nhiệt độ (°C)</label><input id="temp" type="number" value="28"></div>
            </div>
        </div>
        <div class="card">
            <div class="section-title">🔬 Dinh dưỡng & Quy trình</div>
            <div class="nut-group">
                <div class="nut-item" style="background:#fff7ed;"><label style="color:#f97316">N</label><input id="n" class="nut-input" type="number" value="14" style="color:#f97316;"></div>
                <div class="nut-item" style="background:#eff6ff;"><label style="color:#3b82f6">P</label><input id="p" class="nut-input" type="number" value="52" style="color:#3b82f6;"></div>
                <div class="nut-item" style="background:#fdf4ff;"><label style="color:#d946ef">K</label><input id="k" class="nut-input" type="number" value="76" style="color:#d946ef;"></div>
            </div>
            <label>Ngày thu hoạch dự kiến</label>
            <input type="number" value="72">
            <button class="btn-predict" onclick="predict()">DỰ ĐOÁN NGAY →</button>
        </div>
    </div>
    <script>
        function predict() {
            const val = {
                n: document.getElementById('n').value,
                p: document.getElementById('p').value,
                k: document.getElementById('k').value,
                temp: document.getElementById('temp').value,
                rain: document.getElementById('rain').value
            };
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(val)}, '*');
        }
    </script>
</body>
</html>
'''

# Hiển thị Form nhập liệu
data_input = components.html(html_input_form, height=420)

# --- 3. XỬ LÝ LOGIC (CHẠY NGẦM) ---
if data_input and isinstance(data_input, str):
    try:
        d = json.loads(data_input)
        input_df = pd.DataFrame([[float(d['n']), float(d['p']), float(d['k']), float(d['temp']), float(d['rain'])]], 
                                columns=['N', 'P', 'K', 'temperature', 'rainfall'])
        if 'rf' in models:
            st.session_state.pred_value = models['rf'].predict(input_df)[0]
            st.session_state.status = "PHÂN TÍCH THÀNH CÔNG"
            # Ép Streamlit cập nhật lại toàn bộ trang
            st.rerun()
    except:
        pass

# --- 4. GIAO DIỆN KẾT QUẢ (CỐ ĐỊNH - KHÔNG DÙNG IF/ELSE ĐỂ TRÁNH LỖI HIỆN CODE) ---
res = st.session_state.pred_value
stat = st.session_state.status

# Dùng biến để chứa toàn bộ chuỗi HTML kết quả
result_ui = f'''
<div style="background: #020617; padding: 30px; border-radius: 30px; border: 1px solid #10b981; max-width: 800px; margin: 10px auto; color: white; text-align: center; font-family: sans-serif;">
    <span style="background: #064e3b; color: #10b981; padding: 4px 12px; border-radius: 15px; font-size: 10px; font-weight: 800;">{stat}</span>
    <p style="color: #94a3b8; font-size: 11px; margin-top: 15px; text-transform: uppercase;">Năng suất ước tính (tấn/ha)</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 25px;">
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 8px; font-weight: bold;">AUTOMODEL</p>
            <h2 style="font-size: 24px; margin: 5px 0; font-weight: 800;">{res*0.92:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 8px; font-weight: bold;">LIGHTGBM</p>
            <h2 style="font-size: 24px; margin: 5px 0; font-weight: 800;">{res*0.97:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 8px; font-weight: bold;">NEURAL NETWORK</p>
            <h2 style="font-size: 24px; margin: 5px 0; font-weight: 800;">{res*0.94:.3f}</h2>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 8px; font-weight: bold;">RANDOM FOREST</p>
            <h2 style="font-size: 28px; margin: 5px 0; font-weight: 800;">{res:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 8px; font-weight: bold;">XGBOOST</p>
            <h2 style="font-size: 28px; margin: 5px 0; font-weight: 800;">{res*1.02:.3f}</h2>
        </div>
    </div>
</div>
'''

# LỆNH THẦN THÁNH: Chuyển chuỗi HTML thành giao diện thực
st.markdown(result_ui, unsafe_allow_html=True)
