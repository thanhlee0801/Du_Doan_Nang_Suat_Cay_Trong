import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="centered")

# Đường dẫn tới thư mục model
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    if os.path.exists(path):
        models['rf'] = joblib.load(path)
    return models

models = load_models()

# --- 2. GIAO DIỆN NHẬP LIỆU (HTML & CSS) ---
# Thiết kế bo góc 30px, màu sắc hiện đại theo phong cách Dashboard
html_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f8fafc; font-family: 'Inter', sans-serif; padding: 15px; }
        .card { 
            background: white; 
            border-radius: 30px; 
            padding: 35px; 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
            border: 1px solid #f1f5f9;
        }
        label { 
            font-size: 11px; 
            font-weight: 800; 
            color: #64748b; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: block;
        }
        input { 
            border: 1.5px solid #e2e8f0; 
            border-radius: 15px; 
            padding: 12px 15px; 
            width: 100%; 
            margin-bottom: 20px; 
            outline: none; 
            background: #f8fafc;
            transition: all 0.2s;
        }
        input:focus { border-color: #10b981; background: white; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1); }
        button { 
            background: #059669; 
            color: white; 
            width: 100%; 
            padding: 18px; 
            border-radius: 20px; 
            font-weight: 700; 
            font-size: 16px;
            cursor: pointer; 
            border: none; 
            transition: all 0.3s;
            box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.3);
        }
        button:hover { background: #047857; transform: translateY(-2px); box-shadow: 0 20px 25px -5px rgba(5, 150, 105, 0.4); }
        button:active { transform: translateY(0); }
    </style>
</head>
<body>
    <div class="max-w-md mx-auto card">
        <div class="text-center mb-8">
            <h2 style="color:#1e293b; font-size: 24px; font-weight: 900;">AgroPredict <span style="color:#10b981;">AI</span></h2>
            <p style="color:#94a3b8; font-size: 13px; margin-top: 5px;">Hệ thống dự báo năng suất cây trồng</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label>Nitơ (N)</label><input id="n" type="number" value="14" step="any"></div>
            <div><label>Phốt pho (P)</label><input id="p" type="number" value="52" step="any"></div>
        </div>
        
        <label>Kali (K)</label><input id="k" type="number" value="76" step="any">
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label>Nhiệt độ (°C)</label><input id="temp" type="number" value="28" step="any"></div>
            <div><label>Lượng mưa (mm)</label><input id="rain" type="number" value="250" step="any"></div>
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
data_input = components.html(html_form, height=600)

# Vùng chứa kết quả (Sử dụng container để giữ vị trí)
result_area = st.container()

# --- 3. XỬ LÝ DỰ ĐOÁN VÀ HIỂN THỊ KẾT QUẢ ---
if data_input and isinstance(data_input, str):
    try:
        # Giải mã dữ liệu an toàn
        d = json.loads(data_input)
        
        # Chuyển đổi dữ liệu sang DataFrame
        # ĐẢM BẢO TÊN CỘT KHỚP VỚI MODEL CỦA BẠN (N, P, K, temperature, rainfall)
        input_df = pd.DataFrame([[
            float(d['n']), float(d['p']), float(d['k']), 
            float(d['temp']), float(d['rain'])
        ]], columns=['N', 'P', 'K', 'temperature', 'rainfall'])

        if 'rf' in models:
            # Dự đoán năng suất
            prediction = models['rf'].predict(input_df)[0]
            
            # GIAO DIỆN KẾT QUẢ DARK MODE (Như ảnh mẫu)
            result_area.markdown(f'''
            <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); 
                        padding: 45px; border-radius: 35px; color: white; text-align: center; 
                        margin: 25px auto; max-width: 450px; border: 1px solid #10b981;
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                <p style="color: #10b981; font-weight: 900; font-size: 11px; text-transform: uppercase; letter-spacing: 3px; margin: 0;">Phân tích thành công</p>
                
                <div style="margin-top: 30px;">
                    <p style="color: #94a3b8; font-size: 12px; text-transform: uppercase; margin-bottom: 5px;">Năng suất ước tính</p>
                    <h2 style="font-size: 56px; font-weight: 900; margin: 0; color: #ffffff; letter-spacing: -1px;">
                        {prediction:.3f} <span style="font-size: 18px; color: #475569; font-weight: 500;">tấn/ha</span>
                    </h2>
                </div>
                
                <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 30px auto; width: 50%;"></div>
                
                <div style="display: flex; justify-content: center; gap: 20px; align-items: center;">
                    <div style="text-align: center;">
                        <p style="font-size: 9px; color: #64748b; text-transform: uppercase;">Mô hình</p>
                        <p style="font-size: 12px; font-weight: 600; color: #10b981;">Random Forest</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.balloons()
        else:
            result_area.error("⚠️ Lỗi: Không tìm thấy tệp model (.pkl) trong thư mục chỉ định.")

    except Exception as e:
        result_area.error(f"❌ Lỗi hệ thống: {str(e)}")
else:
    # Trạng thái ban đầu khi chưa nhấn nút
    result_area.markdown('''
    <div style="text-align: center; padding: 20px; color: #94a3b8; font-size: 14px; font-style: italic;">
        Hệ thống đang chờ dữ liệu đầu vào...
    </div>
    ''', unsafe_allow_html=True)
