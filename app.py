import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import json # Thêm dòng này ở đầu file app.py

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Đường dẫn tới thư mục model (Đảm bảo đường dẫn này đúng trong Repo của bạn)
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

# --- 2. GIAO DIỆN HTML & CSS (TỐI ƯU THEO ẢNH) ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f0fdf4; margin: 0; padding: 10px; }
        .card-shadow { box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05); }
        .input-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; outline: none; transition: all 0.2s; }
        .input-box:focus { border-color: #10b981; background: white; }
    </style>
</head>
<body>
    <div class="max-w-5xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-extrabold text-slate-800">AgroPredict <span class="text-emerald-500">AI</span></h1>
            <p class="text-slate-500 text-sm mt-2 max-w-lg mx-auto">Ứng dụng công nghệ học máy để tối ưu hóa năng suất nông nghiệp.</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white rounded-[32px] p-8 card-shadow border border-white">
                <div class="flex items-center gap-3 mb-6">
                    <div class="p-3 bg-emerald-50 rounded-2xl text-emerald-600 font-bold">📍</div>
                    <div>
                        <h2 class="font-bold text-slate-800">Môi trường</h2>
                        <p class="text-[10px] text-slate-400 uppercase tracking-widest">Thông tin vùng miền</p>
                    </div>
                </div>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="text-[10px] font-bold text-slate-400 uppercase ml-1">Lượng mưa (mm)</label>
                            <input id="rain" type="number" value="250" class="input-box">
                        </div>
                        <div>
                            <label class="text-[10px] font-bold text-slate-400 uppercase ml-1">Nhiệt độ (°C)</label>
                            <input id="temp" type="number" value="28" class="input-box">
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-[32px] p-8 card-shadow border border-white flex flex-col justify-between">
                <div>
                    <div class="flex items-center gap-3 mb-6">
                        <div class="p-3 bg-blue-50 rounded-2xl text-blue-600 font-bold">🧪</div>
                        <div>
                            <h2 class="font-bold text-slate-800">Dinh dưỡng</h2>
                            <p class="text-[10px] text-slate-400 uppercase tracking-widest">Thông số hóa lý</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-3 mb-6">
                        <div class="bg-orange-50 border border-orange-100 rounded-2xl p-3 text-center">
                            <span class="text-[9px] font-black text-orange-400 block uppercase">N</span>
                            <input id="n" type="number" value="14" class="w-full bg-transparent text-center font-bold text-orange-600 outline-none">
                        </div>
                        <div class="bg-blue-50 border border-blue-100 rounded-2xl p-3 text-center">
                            <span class="text-[9px] font-black text-blue-400 block uppercase">P</span>
                            <input id="p" type="number" value="52" class="w-full bg-transparent text-center font-bold text-blue-600 outline-none">
                        </div>
                        <div class="bg-purple-50 border border-purple-100 rounded-2xl p-3 text-center">
                            <span class="text-[9px] font-black text-purple-400 block uppercase">K</span>
                            <input id="k" type="number" value="76" class="w-full bg-transparent text-center font-bold text-purple-600 outline-none">
                        </div>
                    </div>
                </div>
                <button onclick="predict()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-emerald-200">
                    DỰ ĐOÁN NGAY →
                </button>
            </div>
        </div>
    </div>

<script>
    function predict() {
        const payload = {
            n: parseFloat(document.getElementById('n').value) || 0,
            p: parseFloat(document.getElementById('p').value) || 0,
            k: parseFloat(document.getElementById('k').value) || 0,
            temp: parseFloat(document.getElementById('temp').value) || 0,
            rain: parseFloat(document.getElementById('rain').value) || 0
        };
        // Gửi dạng chuỗi JSON để an toàn tuyệt đối
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: JSON.stringify(payload)
        }, '*');
    }
</script>
</body>
</html>
"""

# Hiển thị giao diện và nhận giá trị
data_input = components.html(html_code, height=520)

# --- 3. XỬ LÝ DỰ ĐOÁN ---
if data_input:
    try:
        # Giải mã dữ liệu từ JSON (để tránh Streamlit hiểu nhầm đối tượng)
        import json
        if isinstance(data_input, str):
            input_dict = json.loads(data_input)
        else:
            # Ép kiểu thủ công về dict thuần túy
            input_dict = dict(data_input) 

        # KHÔNG DÙNG .get() - Dùng cách truy cập trực tiếp bằng ngoặc vuông []
        # Chúng ta dùng try/except nhỏ để gán giá trị mặc định nếu thiếu phím
        try: n = float(input_dict['n'])
        except: n = 0.0
            
        try: p = float(input_dict['p'])
        except: p = 0.0
            
        try: k = float(input_dict['k'])
        except: k = 0.0
            
        try: t = float(input_dict['temp'])
        except: t = 25.0
            
        try: r = float(input_dict['rain'])
        except: r = 100.0

        # Tạo DataFrame (Lưu ý: Tên cột N, P, K... phải khớp với Model của bạn)
        df = pd.DataFrame([{
            'N': n, 'P': p, 'K': k, 
            'temperature': t, 'rainfall': r
        }])

        if models:
            # Thực hiện dự đoán
            res_rf = models['rf'].predict(df)[0]
            
            # Hiển thị kết quả (Giao diện tối màu)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); padding: 30px; border-radius: 25px; color: white; text-align: center; margin-top: 20px;">
                <p style="color: #10b981; font-size: 12px; font-weight: bold; text-transform: uppercase;">Dự đoán thành công</p>
                <h2 style="font-size: 32px; margin: 10px 0;">{res_rf:.3f} <span style="font-size: 14px; color: #94a3b8;">tấn/ha</span></h2>
                <p style="font-size: 10px; color: #64748b;">Kết quả dựa trên mô hình Random Forest</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Không tìm thấy tệp model (.pkl)")

    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
