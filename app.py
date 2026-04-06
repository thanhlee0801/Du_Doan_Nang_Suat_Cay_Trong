import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import json

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Khởi tạo giá trị ban đầu là 0
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = 0.0

# --- 2. FORM NHẬP LIỆU (Giữ đơn giản để test nút) ---
html_input = '''
<div style="padding:20px; background:#f0fdf4; border-radius:15px; border:1px solid #10b981; max-width:400px; margin:auto; font-family:sans-serif;">
    <p style="font-weight:bold; color:#065f46; text-align:center;">TEST NÚT DỰ ĐOÁN</p>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
        <input id="n" type="number" value="14" style="padding:8px;">
        <input id="p" type="number" value="52" style="padding:8px;">
        <input id="k" type="number" value="76" style="padding:8px;">
        <input id="temp" type="number" value="28" style="padding:8px;">
        <input id="rain" type="number" value="250" style="grid-column: span 2; padding:8px;">
    </div>
    <button onclick="predict()" style="width:100%; margin-top:15px; background:#059669; color:white; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
        DỰ ĐOÁN NGAY →
    </button>
</div>
<script>
    function predict() {
        const d = {
            n: document.getElementById('n').value, p: document.getElementById('p').value,
            k: document.getElementById('k').value, temp: document.getElementById('temp').value,
            rain: document.getElementById('rain').value
        };
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(d)}, '*');
    }
</script>
'''

res_js = components.html(html_input, height=250)

# --- 3. XỬ LÝ LOGIC ---
if res_js and isinstance(res_js, str):
    try:
        import tensorflow as tf
        model_path = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/neural_network_model.h5"
        
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            d = json.loads(res_js)
            input_data = np.array([[float(d['n']), float(d['p']), float(d['k']), float(d['temp']), float(d['rain'])]])
            
            prediction = model.predict(input_data)
            st.session_state.ket_qua = float(prediction[0][0])
            st.rerun()
        else:
            st.error(f"Không tìm thấy file model tại: {model_path}")
    except ImportError:
        st.info("🔄 Đang cài đặt thư viện hệ thống... Vui lòng đợi trong giây lát.")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# --- 4. HIỂN THỊ KẾT QUẢ ---
st.markdown(f"""
    <div style="text-align:center; margin-top:30px; font-family:sans-serif;">
        <h1 style="color:#10b981; font-size:50px;">{st.session_state.ket_qua:.3f}</h1>
        <p style="color:#64748b;">Năng suất dự kiến (tấn/ha)</p>
    </div>
""", unsafe_allow_html=True)
