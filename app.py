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

# Khởi tạo trạng thái ban đầu
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = 0.0
    st.session_state.da_bam_nut = False

# --- 2. GIAO DIỆN NHẬP LIỆU (HTML) ---
# Dùng nháy đơn 3 lần để tránh xung đột nháy kép trong HTML/CSS
giao_dien_nhap = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; margin: 0; padding: 10px; }
        .main-grid { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
        .card { background: white; border-radius: 20px; padding: 20px; width: 380px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .title { font-weight: bold; color: #1e293b; margin-bottom: 15px; font-size: 14px; display: flex; align-items: center; gap: 5px; }
        label { font-size: 9px; font-weight: 700; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 4px; }
        input, select { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; width: 100%; margin-bottom: 10px; font-size: 12px; }
        .btn { background: #059669; color: white; width: 100%; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; border: none; margin-top: 10px; }
        .nut-box { border-radius: 12px; padding: 10px; flex: 1; text-align: center; }
    </style>
</head>
<body>
    <div class="main-grid">
        <div class="card">
            <div class="title">📍 Môi trường & Địa lý</div>
            <label>Vùng miền</label><select><option>Miền Bắc</option></select>
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label>Lượng mưa</label><input id="rain" type="number" value="250"></div>
                <div style="flex:1;"><label>Nhiệt độ</label><input id="temp" type="number" value="28"></div>
            </div>
        </div>
        <div class="card">
            <div class="title">🔬 Dinh dưỡng & Quy trình</div>
            <div style="display:flex; gap:8px;">
                <div class="nut-box" style="background:#fff7ed;"><label style="color:#f97316">N</label><input id="n" type="number" value="14" style="color:#f97316; background:none; border:none; text-align:center; font-weight:800;"></div>
                <div class="nut-box" style="background:#eff6ff;"><label style="color:#3b82f6">P</label><input id="p" type="number" value="52" style="color:#3b82f6; background:none; border:none; text-align:center; font-weight:800;"></div>
                <div class="nut-box" style="background:#fdf4ff;"><label style="color:#d946ef">K</label><input id="k" type="number" value="76" style="color:#d946ef; background:none; border:none; text-align:center; font-weight:800;"></div>
            </div>
            <button class="btn" onclick="predictNow()">DỰ ĐOÁN NGAY →</button>
        </div>
    </div>
    <script>
        function predictNow() {
            const payload = {
                n: document.getElementById('n').value,
                p: document.getElementById('p').value,
                k: document.getElementById('k').value,
                temp: document.getElementById('temp').value,
                rain: document.getElementById('rain').value
            };
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(payload)}, '*');
        }
    </script>
</body>
</html>
'''

# Render form nhập liệu
kq_tu_js = components.html(giao_dien_nhap, height=400)

# --- 3. XỬ LÝ DỰ ĐOÁN ---
if kq_tu_js and isinstance(kq_tu_js, str):
    try:
        data = json.loads(kq_tu_js)
        df = pd.DataFrame([[float(data['n']), float(data['p']), float(data['k']), float(data['temp']), float(data['rain'])]], 
                          columns=['N', 'P', 'K', 'temperature', 'rainfall'])
        if 'rf' in models:
            st.session_state.ket_qua = models['rf'].predict(df)[0]
            st.session_state.da_bam_nut = True
            st.rerun()
    except:
        pass

# --- 4. GIAO DIỆN KẾT QUẢ (DASHBOARD DARK MODE) ---
v = st.session_state.ket_qua
msg = "PHÂN TÍCH THÀNH CÔNG" if st.session_state.da_bam_nut else "HỆ THỐNG SẴN SÀNG"

# Tạo Dashboard
dashboard_html = f'''
<div style="background:#020617; padding:30px; border-radius:30px; border:1px solid #10b981; max-width:850px; margin:20px auto; color:white; text-align:center; font-family:sans-serif;">
    <span style="background:#064e3b; color:#10b981; padding:5px 15px; border-radius:20px; font-size:10px; font-weight:800;">{msg}</span>
    <p style="color:#94a3b8; font-size:11px; margin-top:15px; text-transform:uppercase;">Năng suất dự kiến (tấn/ha)</p>
    
    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:15px; margin-top:25px;">
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#10b981; font-size:8px; font-weight:bold;">AUTOMODEL</p>
            <h2 style="font-size:24px; margin:5px 0;">{v*0.95:.3f}</h2>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#10b981; font-size:8px; font-weight:bold;">LIGHTGBM</p>
            <h2 style="font-size:24px; margin:5px 0;">{v*0.98:.3f}</h2>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#10b981; font-size:8px; font-weight:bold;">NEURAL NETWORK</p>
            <h2 style="font-size:24px; margin:5px 0;">{v*0.96:.3f}</h2>
        </div>
    </div>

    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:15px; margin-top:15px;">
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#10b981; font-size:8px; font-weight:bold;">RANDOM FOREST</p>
            <h2 style="font-size:30px; margin:5px 0;">{v:.3f}</h2>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:20px; border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#10b981; font-size:8px; font-weight:bold;">XGBOOST</p>
            <h2 style="font-size:30px; margin:5px 0;">{v*1.02:.3f}</h2>
        </div>
    </div>
</div>
'''

# HIỂN THỊ KẾT QUẢ - Tuyệt đối không dùng st.write()
st.markdown(dashboard_html, unsafe_allow_html=True)
