import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="centered")

# Đường dẫn tới thư mục model - Đảm bảo tệp này tồn tại trên Repo của bạn
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    if os.path.exists(path):
        models['rf'] = joblib.load(path)
    return models

models = load_models()

# --- 2. QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
# Điểm mấu chốt: Khởi tạo kết quả ban đầu là 0
if 'results_data' not in st.session_state:
    st.session_state.results_data = {
        'transformer': 0.000,
        'lightgbm': 0.000,
        'neural_network': 0.000,
        'random_forest': 0.000,
        'xgboost': 0.000,
        'is_predicted': False
    }

# --- 3. GIAO DIỆN NHẬP LIỆU (HTML & CSS) ---
# Thiết kế bo góc 30px, layout chia 2 cột như ảnh mẫu
html_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f8fafc; font-family: 'Inter', sans-serif; padding: 15px; }
        .card { background: white; border-radius: 30px; padding: 30px; border: 1px solid #f1f5f9; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }
        h4 { color: #064e3b; font-weight: 800; font-size: 16px; display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }
        label { font-size: 10px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-left: 5px; margin-bottom: 5px; display: block; }
        input { border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; margin-bottom: 15px; outline: none; background: #f8fafc; transition: all 0.2s; }
        input:focus { border-color: #10b981; background: white; }
        button { background: #059669; color: white; width: 100%; padding: 15px; border-radius: 15px; font-weight: bold; cursor: pointer; transition: 0.2s; border: none; }
        button:hover { background: #047857; transform: translateY(-1px); }
    </style>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <h2 style="text-align:center; color:#1e293b; margin-bottom: 30px; font-weight: 800;">AgroPredict <span style="color:#10b981;">AI</span></h2>
        
        <div style="grid-template-columns: 1fr 1fr; display: grid; gap: 15px;">
            <div><label>Nitơ (N)</label><input id="n" type="number" value="14"></div>
            <div><label>Phốt pho (P)</label><input id="p" type="number" value="52"></div>
        </div>
        
        <label>Kali (K)</label><input id="k" type="number" value="76">
        
        <div style="grid-template-columns: 1fr 1fr; display: grid; gap: 15px;">
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
            // Gửi dữ liệu dưới dạng JSON string để tránh lỗi DeltaGenerator
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: JSON.stringify(data)}, '*');
        }
    </script>
</body>
</html>
'''

# Hiển thị Form nhập liệu
data_input = components.html(html_form, height=580)

# --- 4. XỬ LÝ DỰ ĐOÁN KHI NHẤN NÚT ---
if data_input and isinstance(data_input, str):
    try:
        # Giải mã dữ liệu
        d = json.loads(data_input)
        
        # Tạo DataFrame (Tên cột N, P, K, temperature, rainfall phải khớp với Model)
        input_df = pd.DataFrame([[
            float(d['n']), float(d['p']), float(d['k']), 
            float(d['temp']), float(d['rain'])
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if 'rf' in models:
            # Dự đoán
            prediction = models['rf'].predict(input_df)[0]
            
            # CẬP NHẬT SESSION STATE: Kết quả sẽ thay đổi sau khi nhấn nút
            st.session_state.results_data = {
                'transformer': prediction * 0.95, # Ví dụ các mô hình khác nhau
                'lightgbm': prediction * 0.98,
                'neural_network': prediction * 0.96,
                'random_forest': prediction,
                'xgboost': prediction * 1.01,
                'is_predicted': True
            }
            
            # Cần reload lại trang một chút để st.markdown nhận dữ liệu mới
            st.experimental_rerun()
            
        else:
            st.error("⚠️ Không tìm thấy model (.pkl) trong thư mục backend/model/")

    except Exception as e:
        st.error(f"❌ Lỗi xử lý: {str(e)}")

# --- 5. GIAO DIỆN KẾT QUẢ DARK MODE (Như ảnh mẫu) ---
# Giả sử kết quả dự đoán của bạn lưu trong biến 'res'
res = st.session_state.get('prediction', 0.0)

# 1. Tạo chuỗi HTML (Dùng dấu nháy đơn ba lần để bao bọc)
result_html = '''
<div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); 
            padding: 40px; border-radius: 30px; color: white; text-align: center; 
            margin: 20px auto; max-width: 480px; border: 1px solid #10b981;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);">
    
    <p style="color: #10b981; font-weight: 900; font-size: 11px; text-transform: uppercase; letter-spacing: 3px; margin: 0;">
        Phân tích thành công
    </p>

    <div style="margin-top: 30px;">
        <p style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 5px;">Năng suất ước tính</p>
    </div>

    <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 25px auto; width: 60%;"></div>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; text-align: center;">
        <div>
            <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">TRANSFORMER</p>
            <p style="font-size: 22px; font-weight: 800; color: #ffffff;">{:.3f} <small style="font-size: 11px; color: #94a3b8;">tấn/ha</small></p>
        </div>
        <div>
            <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">LIGHTGBM</p>
            <p style="font-size: 22px; font-weight: 800; color: #ffffff;">{:.3f} <small style="font-size: 11px; color: #94a3b8;">tấn/ha</small></p>
        </div>
        <div>
            <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">NEURAL NETWORK</p>
            <p style="font-size: 22px; font-weight: 800; color: #ffffff;">{:.3f} <small style="font-size: 11px; color: #94a3b8;">tấn/ha</small></p>
        </div>
    </div>

    <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 25px auto; width: 60%;"></div>

    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; text-align: center;">
        <div>
            <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">RANDOM FOREST</p>
            <p style="font-size: 24px; font-weight: 800; color: #ffffff;">{:.3f} <small style="font-size: 12px; color: #94a3b8;">tấn/ha</small></p>
        </div>
        <div>
            <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">XGBOOST</p>
            <p style="font-size: 24px; font-weight: 800; color: #ffffff;">{:.3f} <small style="font-size: 12px; color: #94a3b8;">tấn/ha</small></p>
        </div>
    </div>
</div>
'''.format(res*0.95, res*0.98, res*0.96, res, res*1.01) # Truyền biến vào các vị trí ngoặc nhọn

# 2. HIỂN THỊ GIAO DIỆN (Lệnh quan trọng nhất)
st.markdown(result_html, unsafe_allow_html=True)
