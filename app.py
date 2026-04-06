import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import json

# --- 1. LOAD MODEL (.H5) ---
@st.cache_resource
def load_keras_model():
    # Đường dẫn tính từ gốc thư mục GitHub của bạn
    model_path = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/neural_network_model.h5"
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    return None

model = load_keras_model()

# Khởi tạo giá trị ban đầu là 0
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = 0.0

# --- 2. HIỂN THỊ THÔNG BÁO LỖI NẾU THIẾU FILE ---
if model is None:
    st.error("❌ Không tìm thấy file neural_network_model.h5. Hãy đảm bảo bạn đã giải nén folder hoặc để đúng đường dẫn.")
    st.stop()

# --- 3. FORM NHẬP LIỆU (TỐI GIẢN ĐỂ TEST NÚT BẤM) ---
html_input = '''
    <div style="padding:20px; background:#f0fdf4; border-radius:15px; border:1px solid #10b981; max-width:400px; margin:auto;">
        <p style="font-weight:bold; color:#065f46; text-align:center;">KIỂM TRA NÚT DỰ ĐOÁN</p>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <input id="n" type="number" value="14" placeholder="N">
            <input id="p" type="number" value="52" placeholder="P">
            <input id="k" type="number" value="76" placeholder="K">
            <input id="temp" type="number" value="28" placeholder="Temp">
            <input id="rain" type="number" value="250" placeholder="Rain" style="grid-column: span 2;">
        </div>
        <button onclick="predict()" style="width:100%; margin-top:15px; background:#059669; color:white; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
            DỰ ĐOÁN NGAY →
        </button>
    </div>
    <script>
        function predict() {
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

data_js = components.html(html_input, height=250)

# --- 4. XỬ LÝ DỮ LIỆU KHI BẤM NÚT ---
if data_js and isinstance(data_js, str):
    try:
        payload = json.loads(data_js)
        # Chuyển dữ liệu sang mảng Numpy cho Neural Network
        input_array = np.array([[
            float(payload['n']), float(payload['p']), float(payload['k']), 
            float(payload['temp']), float(payload['rain'])
        ]])
        
        # Dự đoán
        prediction = model.predict(input_array)
        st.session_state.ket_qua = float(prediction[0][0])
        st.rerun()
    except Exception as e:
        st.error(f"Lỗi dự đoán: {e}")

# --- 5. HIỂN THỊ SỐ KIỂM TRA ---
st.markdown(f"""
    <div style="text-align:center; margin-top:20px;">
        <h2 style="color:#10b981;">Kết quả: {st.session_state.ket_qua:.3f} tấn/ha</h2>
        <p style="color:#64748b;">(Nếu số này nhảy từ 0 lên số khác khi bấm nút là THÀNH CÔNG)</p>
    </div>
""", unsafe_allow_html=True)
