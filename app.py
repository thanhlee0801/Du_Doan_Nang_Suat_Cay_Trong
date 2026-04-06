import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os

# 1. Cấu hình đường dẫn Model
# Tính từ vị trí file app.py
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    files = {
        'rf': 'random_forest_model.pkl',
        'xgb': 'xgboost_model.pkl',
        'lgbm': 'lightgbm_model.pkl'
    }
    for key, name in files.items():
        path = os.path.join(MODEL_DIR, name)
        if os.path.exists(path):
            models[key] = joblib.load(path)
    return models

models = load_models()

# 2. Hàm dự đoán (Backend thực thụ)
def xử_lý_dự_đoán(data):
    if not models: return None
    # Chuyển dữ liệu từ JS sang DataFrame (phải khớp tên cột khi train)
    input_df = pd.DataFrame([{
        'N': data['n'], 'P': data['p'], 'K': data['k'],
        'temperature': data['temp'], 'rainfall': data['rain']
    }])
    
    results = {}
    for name, model in models.items():
        results[name] = round(model.predict(input_df)[0], 3)
    return results

# 3. Giao diện HTML (Frontend)
html_ui = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; padding: 20px; }
        .card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <div class="card max-w-2xl mx-auto">
        <h2 class="text-xl font-bold mb-4 text-emerald-700">Nhập thông số nông nghiệp</h2>
        <div class="grid grid-cols-2 gap-4">
            <input id="n" type="number" placeholder="Nitơ (N)" class="border p-2 rounded">
            <input id="p" type="number" placeholder="Phốt pho (P)" class="border p-2 rounded">
            <input id="k" type="number" placeholder="Kali (K)" class="border p-2 rounded">
            <input id="temp" type="number" placeholder="Nhiệt độ" class="border p-2 rounded">
            <input id="rain" type="number" placeholder="Lượng mưa" class="border p-2 rounded">
        </div>
        <button onclick="predict()" class="w-full mt-4 bg-emerald-600 text-white py-2 rounded-lg font-bold">DỰ ĐOÁN</button>
    </div>

    <script>
        function predict() {
            const payload = {
                n: parseFloat(document.getElementById('n').value || 0),
                p: parseFloat(document.getElementById('p').value || 0),
                k: parseFloat(document.getElementById('k').value || 0),
                temp: parseFloat(document.getElementById('temp').value || 0),
                rain: parseFloat(document.getElementById('rain').value || 0)
            };
            // Gửi sang Streamlit (Python)
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: payload
            }, '*');
        }
    </script>
</body>
</html>
"""

# Hiển thị UI và nhận giá trị trả về từ JS
data_from_ui = components.html(html_ui, height=400)

# 4. Hiển thị kết quả Backend
if data_from_ui:
    ket_qua = xử_lý_dự_đoán(data_from_ui)
    if ket_qua:
        st.balloons()
        st.write("### 📊 Kết quả dự đoán từ Backend:")
        c1, c2, c3 = st.columns(3)
        c1.metric("Random Forest", f"{ket_qua.get('rf')} tấn/ha")
        c2.metric("XGBoost", f"{ket_qua.get('xgb')} tấn/ha")
        c3.metric("LightGBM", f"{ket_qua.get('lgbm')} tấn/ha")
