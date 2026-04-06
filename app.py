import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH & LOAD MODEL ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Đường dẫn tới thư mục model của bạn (sửa cho đúng với máy bạn)
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    # Danh sách các file model trong repo của bạn
    model_files = {
        'rf': 'random_forest_model.pkl',
        'xgb': 'xgboost_model.pkl',
        'lgbm': 'lightgbm_model.pkl'
    }
    for key, filename in model_files.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            models[key] = joblib.load(path)
    return models

models = load_models()

# --- 2. LOGIC DỰ ĐOÁN (BACKEND) ---
def predict_yield(data):
    # Tạo DataFrame từ dữ liệu JS gửi sang
    # Lưu ý: Tên cột phải khớp 100% với lúc bạn train model (N, P, K, temperature, rainfall, v.v.)
    df = pd.DataFrame([{
        'N': data['n'],
        'P': data['p'],
        'K': data['k'],
        'temperature': data['temp'],
        'rainfall': data['rain']
    }])
    
    results = {}
    if 'rf' in models: results['rf'] = round(models['rf'].predict(df)[0], 3)
    if 'xgb' in models: results['xgb'] = round(models['xgb'].predict(df)[0], 3)
    if 'lgbm' in models: results['lgbm'] = round(models['lgbm'].predict(df)[0], 3)
    
    return results

# --- 3. GIAO DIỆN HTML + JS (FRONTEND) ---
# Dùng thư viện Tailwind CSS để vẽ giao diện giống ảnh 100%
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f0fdf4; margin:0; padding:20px; }}
        .gradient-bg {{ background: linear-gradient(135deg, #064e3b 0%, #020617 100%); }}
        .input-style {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px; width: 100%; outline: none; }}
    </style>
</head>
<body>
    <div class="max-w-5xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-black text-slate-800">AgroPredict <span class="text-emerald-500">AI</span></h1>
            <p class="text-slate-500 text-sm mt-2">Dự đoán năng suất dựa trên dữ liệu thời gian thực</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-white p-8 rounded-[32px] shadow-sm border border-white">
                <h3 class="font-bold text-slate-800 mb-6 flex items-center gap-2">📍 Môi trường</h3>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div><label class="text-[10px] font-bold text-slate-400 uppercase">Lượng mưa</label>
                        <input id="rain" type="number" value="250" class="input-style"></div>
                        <div><label class="text-[10px] font-bold text-slate-400 uppercase">Nhiệt độ</label>
                        <input id="temp" type="number" value="28" class="input-style"></div>
                    </div>
                </div>
            </div>

            <div class="bg-white p-8 rounded-[32px] shadow-sm border border-white">
                <h3 class="font-bold text-slate-800 mb-6 flex items-center gap-2">🧪 Dinh dưỡng</h3>
                <div class="grid grid-cols-3 gap-3 mb-6">
                    <div class="bg-orange-50 p-3 rounded-xl text-center"><span class="text-[9px] font-bold text-orange-400 uppercase">N</span>
                    <input id="n" type="number" value="14" class="w-full bg-transparent text-center font-bold text-orange-600 outline-none"></div>
                    <div class="bg-blue-50 p-3 rounded-xl text-center"><span class="text-[9px] font-bold text-blue-400 uppercase">P</span>
                    <input id="p" type="number" value="52" class="w-full bg-transparent text-center font-bold text-blue-600 outline-none"></div>
                    <div class="bg-purple-50 p-3 rounded-xl text-center"><span class="text-[9px] font-bold text-purple-400 uppercase">K</span>
                    <input id="k" type="number" value="76" class="w-full bg-transparent text-center font-bold text-purple-600 outline-none"></div>
                </div>
                <button onclick="sendDataToStreamlit()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-emerald-100">
                    DỰ ĐOÁN NGAY →
                </button>
            </div>
        </div>
    </div>

    <script>
        function sendDataToStreamlit() {{
            const data = {{
                rain: parseFloat(document.getElementById('rain').value),
                temp: parseFloat(document.getElementById('temp').value),
                n: parseFloat(document.getElementById('n').value),
                p: parseFloat(document.getElementById('p').value),
                k: parseFloat(document.getElementById('k').value)
            }};
            // Gửi dữ liệu về Python
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: data
            }}, '*');
        }}
    </script>
</body>
</html>
"""

# Hiển thị Component HTML và nhận dữ liệu từ JS
val = components.html(html_code, height=550)

# --- 4. XỬ LÝ DỰ ĐOÁN KHI NHẬN ĐƯỢC DỮ LIỆU ---
if val:
    res = predict_yield(val)
    
    # Hiển thị bảng kết quả đẹp mắt phía dưới bằng Streamlit
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); padding: 40px; border-radius: 32px; color: white; text-align: center;">
        <span style="background: #10b981; font-size: 10px; font-weight: 900; padding: 5px 15px; border-radius: 20px; text-transform: uppercase;">Phân tích thành công</span>
        <h3 style="margin-top: 20px; color: #94a3b8; font-size: 12px; letter-spacing: 2px;">NĂNG SUẤT ƯỚC TÍNH TỪ CÁC MÔ HÌNH</h3>
        <div style="display: flex; justify-content: space-around; margin-top: 30px; flex-wrap: wrap; gap: 20px;">
            <div><p style="color:#10b981; font-size:10px; font-weight:bold;">RANDOM FOREST</p><p style="font-size:28px; font-weight:bold;">{res.get('rf', 0)} <small style="font-size:12px; color:#64748b;">tấn/ha</small></p></div>
            <div><p style="color:#10b981; font-size:10px; font-weight:bold;">XGBOOST</p><p style="font-size:28px; font-weight:bold;">{res.get('xgb', 0)} <small style="font-size:12px; color:#64748b;">tấn/ha</small></p></div>
            <div><p style="color:#10b981; font-size:10px; font-weight:bold;">LIGHTGBM</p><p style="font-size:28px; font-weight:bold;">{res.get('lgbm', 0)} <small style="font-size:12px; color:#64748b;">tấn/ha</small></p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
