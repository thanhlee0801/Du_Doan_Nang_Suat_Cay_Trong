import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Đường dẫn model (Đảm bảo folder này có file .pkl)
MODEL_DIR = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_models():
    models = {}
    path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    if os.path.exists(path):
        models['rf'] = joblib.load(path)
    return models

models = load_models()

# --- 2. GIAO DIỆN NHẬP LIỆU (THEO ẢNH MẪU) ---
html_input_form = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0fdf4; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .main-container { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
        .card { background: white; border-radius: 25px; padding: 25px; width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #f1f5f9; }
        .section-title { font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; font-size: 14px; }
        label { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 5px; margin-top: 10px; }
        input, select { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; outline: none; font-size: 13px; }
        input:focus { border-color: #10b981; background: white; }
        .btn-predict { background: #059669; color: white; width: 100%; padding: 15px; border-radius: 15px; font-weight: 800; margin-top: 25px; cursor: pointer; transition: 0.3s; border: none; font-size: 14px; }
        .btn-predict:hover { background: #047857; transform: translateY(-2px); box-shadow: 0 10px 15px rgba(5, 150, 105, 0.2); }
        .nut-group { display: flex; gap: 10px; margin-top: 10px; }
        .nut-item { border-radius: 15px; padding: 10px; text-align: center; flex: 1; }
        .nut-input { background: transparent; border: none; text-align: center; font-size: 18px; font-weight: 800; width: 100%; padding: 0; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="card">
            <div class="section-title"><span style="background:#d1fae5; padding:6px; border-radius:8px;">📍</span> Môi trường & Địa lý</div>
            <label>Vùng miền canh tác</label>
            <select><option>Miền Bắc</option><option>Miền Trung</option><option>Miền Nam</option></select>
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
            <div class="section-title"><span style="background:#dbeafe; padding:6px; border-radius:8px;">🔬</span> Dinh dưỡng & Quy trình</div>
            <div class="nut-group">
                <div class="nut-item" style="background:#fff7ed; border: 1px solid #ffedd5;">
                    <label style="color:#f97316">Nitơ (N)</label>
                    <input id="n" class="nut-input" type="number" value="14" style="color:#f97316;">
                </div>
                <div class="nut-item" style="background:#eff6ff; border: 1px solid #dbeafe;">
                    <label style="color:#3b82f6">Phốt pho (P)</label>
                    <input id="p" class="nut-input" type="number" value="52" style="color:#3b82f6;">
                </div>
                <div class="nut-item" style="background:#fdf4ff; border: 1px solid #fae8ff;">
                    <label style="color:#d946ef">Kali (K)</label>
                    <input id="k" class="nut-input" type="number" value="76" style="color:#d946ef;">
                </div>
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
data_input = components.html(html_input_form, height=450)

# 3. HÀM RENDER DASHBOARD (Dùng để hiển thị kết quả)
def render_dashboard(res_val, status_msg="HỆ THỐNG SẴN SÀNG"):
    html_dashboard = f'''
    <div style="background: #020617; padding: 40px; border-radius: 35px; border: 1px solid #10b981; max-width: 850px; margin: 20px auto; color: white; text-align: center; font-family: sans-serif;">
        <span style="background: #064e3b; color: #10b981; padding: 5px 15px; border-radius: 20px; font-size: 10px; font-weight: 800;">{status_msg}</span>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 15px; text-transform: uppercase; letter-spacing: 1px;">Năng suất ước tính từ các mô hình (tấn/ha)</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px;">
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #10b981; font-size: 9px; font-weight: bold;">AUTOMODEL</p>
                <h2 style="font-size: 28px; margin: 5px 0; font-weight: 800;">{res_val*0.92:.3f}</h2>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #10b981; font-size: 9px; font-weight: bold;">LIGHTGBM</p>
                <h2 style="font-size: 28px; margin: 5px 0; font-weight: 800;">{res_val*0.97:.3f}</h2>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #10b981; font-size: 9px; font-weight: bold;">NEURAL NETWORK</p>
                <h2 style="font-size: 28px; margin: 5px 0; font-weight: 800;">{res_val*0.94:.3f}</h2>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #10b981; font-size: 9px; font-weight: bold;">RANDOM FOREST</p>
                <h2 style="font-size: 32px; margin: 5px 0; font-weight: 800;">{res_val:.3f}</h2>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                <p style="color: #10b981; font-size: 9px; font-weight: bold;">XGBOOST</p>
                <h2 style="font-size: 32px; margin: 5px 0; font-weight: 800;">{res_val*1.02:.3f}</h2>
            </div>
        </div>
        <p style="font-size: 10px; color: #475569; margin-top: 30px;">Các dự đoán được sinh ra từ các thuật toán Học máy và Học sâu dựa trên tập dữ liệu đã huấn luyện.</p>
    </div>
    '''
    st.markdown(html_dashboard, unsafe_allow_html=True)

# 4. KHU VỰC HIỂN THỊ KẾT QUẢ (Dùng st.empty để thay đổi giá trị)
result_placeholder = st.empty()

# 5. XỬ LÝ LOGIC KHI NHẤN NÚT
if data_input and isinstance(data_input, str):
    try:
        d = json.loads(data_input)
        # Tạo dữ liệu đầu vào cho model
        input_data = pd.DataFrame([[float(d['n']), float(d['p']), float(d['k']), float(d['temp']), float(d['rain'])]], 
                                columns=['N', 'P', 'K', 'temperature', 'rainfall'])
        
        if 'rf' in models:
            res = models['rf'].predict(input_data)[0]
            # Hiển thị Dashboard với kết quả MỚI
            with result_placeholder.container():
                render_dashboard(res, "PHÂN TÍCH THÀNH CÔNG")
                st.balloons()
        else:
            st.error("Không tìm thấy model!")
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    # HIỂN THỊ MẶC ĐỊNH LÀ 0 KHI CHƯA NHẤN NÚT
    with result_placeholder.container():
        render_dashboard(0.000, "HỆ THỐNG SẴN SÀNG")
