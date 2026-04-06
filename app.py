import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os

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
        // Lấy giá trị và ép kiểu số thực ngay tại đây
        const payload = {
            n: parseFloat(document.getElementById('n').value) || 0,
            p: parseFloat(document.getElementById('p').value) || 0,
            k: parseFloat(document.getElementById('k').value) || 0,
            temp: parseFloat(document.getElementById('temp').value) || 25,
            rain: parseFloat(document.getElementById('rain').value) || 100
        };

        // Gửi thông điệp chuẩn cho Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: payload
        }, '*');
    }
</script>
</body>
</html>
"""

# Hiển thị giao diện và nhận giá trị
data_input = components.html(html_code, height=520)

# --- 3. XỬ LÝ DỰ ĐOÁN & HIỂN THỊ KẾT QUẢ ---

# Kiểm tra dữ liệu thô từ component
if data_input:
    try:
        # Ép kiểu dữ liệu về dict nếu nó đang ở dạng proxy hoặc string
        if not isinstance(data_input, dict):
            import json
            # Thử convert nếu dữ liệu bị gửi về dạng chuỗi JSON
            input_dict = dict(data_input) 
        else:
            input_dict = data_input

        # Trích xuất dữ liệu an toàn
        val_n = float(input_dict.get('n', 0))
        val_p = float(input_dict.get('p', 0))
        val_k = float(input_dict.get('k', 0))
        val_t = float(input_dict.get('temp', 0))
        val_r = float(input_dict.get('rain', 0))

        # Tạo DataFrame (Lưu ý: Tên cột phải khớp với Model của bạn)
        df = pd.DataFrame([{
            'N': val_n,
            'P': val_p,
            'K': val_k,
            'temperature': val_t,
            'rainfall': val_r
        }])

        # Thực hiện dự đoán
        if models:
            # Hiển thị vùng kết quả
            st.markdown("### 📊 Kết quả dự đoán")
            res_rf = models['rf'].predict(df)[0]
            st.success(f"Năng suất dự kiến: {res_rf:.3f} tấn/ha")
        else:
            st.error("Không tìm thấy model (.pkl)")

    except Exception as e:
        st.error(f"Lỗi xử lý dữ liệu: {e}")
        st.write("Dữ liệu thô nhận được:", data_input) # Dòng này để debug
