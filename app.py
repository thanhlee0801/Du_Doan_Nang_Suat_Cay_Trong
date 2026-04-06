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
# Dùng nháy đơn 3 lần (''') để bao bọc HTML có chứa nháy kép (")
html_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: sans-serif; padding: 10px; }
        .card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        input { border: 1px solid #ddd; border-radius: 8px; padding: 8px; width: 100%; margin-bottom: 10px; }
        button { background: #10b981; color: white; width: 100%; padding: 12px; border-radius: 10px; font-weight: bold; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <h3 style="text-align:center; color:#065f46;">Thông số nông nghiệp</h3>
        <input id="n" type="number" placeholder="N" value="14">
        <input id="p" type="number" placeholder="P" value="52">
        <input id="k" type="number" placeholder="K" value="76">
        <input id="temp" type="number" placeholder="Temp" value="28">
        <input id="rain" type="number" placeholder="Rain" value="250">
        <button onclick="send()">DỰ ĐOÁN NGAY</button>
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

data_input = components.html(html_form, height=450)

# --- 3. XỬ LÝ DỰ ĐOÁN ---
if data_input:
    try:
        # Giải mã JSON
        d = json.loads(data_input)
        
        # Tạo DataFrame - ĐẢM BẢO TÊN CỘT KHỚP VỚI MODEL CỦA BẠN
        df = pd.DataFrame([[
            float(d['n']), float(d['p']), float(d['k']), 
            float(d['temp']), float(d['rain'])
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if 'rf' in models:
            res = models['rf'].predict(df)[0]
            
            # CÁCH FIX LỖI SYNTAX: Dùng hàm .format() thay vì f-string trực tiếp trong markdown
            display_html = '''
            <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); 
                        padding: 30px; border-radius: 20px; color: white; text-align: center; margin-top: 20px;">
                <p style="color: #10b981; font-weight: bold;">KẾT QUẢ PHÂN TÍCH</p>
                <h2 style="font-size: 35px; margin: 10px 0;">{:.3f} <span style="font-size: 15px;">tấn/ha</span></h2>
            </div>
            '''.format(res)
            
            st.markdown(display_html, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Không tìm thấy model (.pkl)")

    except Exception as e:
        st.error(f"Lỗi: {e}")
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
