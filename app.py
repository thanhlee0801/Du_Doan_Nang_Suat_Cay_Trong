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
            const data = {
                n: parseFloat(document.getElementById('n').value),
                p: parseFloat(document.getElementById('p').value),
                k: parseFloat(document.getElementById('k').value),
                temp: parseFloat(document.getElementById('temp').value),
                rain: parseFloat(document.getElementById('rain').value)
            };
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: data
            }, '*');
        }
    </script>
</body>
</html>
"""

# Hiển thị giao diện và nhận giá trị
data_input = components.html(html_code, height=520)

# --- 3. XỬ LÝ DỰ ĐOÁN & HIỂN THỊ KẾT QUẢ ---

# Bước 1: Kiểm tra xem data_input có dữ liệu từ HTML gửi sang không
if data_input is not None:
    # QUAN TRỌNG: Đảm bảo data_input là một Dictionary của Python
    if isinstance(data_input, dict):
        try:
            # Lấy giá trị an toàn từ Dictionary
            # Nếu không tìm thấy phím 'n', nó sẽ lấy giá trị mặc định là 0
            n = data_input.get('n', 0)
            p = data_input.get('p', 0)
            k = data_input.get('k', 0)
            t = data_input.get('temp', 0)
            r = data_input.get('rain', 0)

            # Bước 2: Tạo DataFrame (Tên cột PHẢI khớp với lúc bạn Train Model)
            # Ví dụ: Nếu lúc train bạn đặt tên là 'Nhiet_Do' thì phải sửa 'temperature' thành 'Nhiet_Do'
            df = pd.DataFrame([{
                'N': n,
                'P': p,
                'K': k,
                'temperature': t,
                'rainfall': r
            }])

            # Bước 3: Kiểm tra Model và Dự đoán
            if models:
                res_rf = models['rf'].predict(df)[0] if 'rf' in models else 0
                res_xgb = models['xgb'].predict(df)[0] if 'xgb' in models else 0
                res_lgbm = models['lgbm'].predict(df)[0] if 'lgbm' in models else 0

                # Bước 4: Hiển thị giao diện kết quả (Card tối màu)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #064e3b 0%, #020617 100%); padding: 40px; border-radius: 32px; color: white; text-align: center; margin-top: 20px;">
                    <p style="color: #10b981; font-size: 10px; font-weight: 900; text-transform: uppercase;">Phân tích thành công</p>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px;">
                        <div>
                            <p style="font-size: 9px; color: #94a3b8;">RANDOM FOREST</p>
                            <p style="font-size: 20px; font-weight: bold;">{res_rf:.3f} <small style="font-size: 10px;">tấn/ha</small></p>
                        </div>
                        <div>
                            <p style="font-size: 9px; color: #10b981;">XGBOOST</p>
                            <p style="font-size: 20px; font-weight: bold;">{res_xgb:.3f} <small style="font-size: 10px;">tấn/ha</small></p>
                        </div>
                        <div>
                            <p style="font-size: 9px; color: #94a3b8;">LIGHTGBM</p>
                            <p style="font-size: 20px; font-weight: bold;">{res_lgbm:.3f} <small style="font-size: 10px;">tấn/ha</small></p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Không tìm thấy các file model (.pkl).")
        
        except Exception as e:
            st.error(f"Lỗi logic dự đoán: {e}")
    else:
        st.warning("Dữ liệu từ giao diện gửi về không đúng định dạng.")
else:
    # Trạng thái ban đầu khi chưa nhấn nút
    st.info("💡 Mẹo: Nhập đầy đủ thông số và nhấn 'DỰ ĐOÁN NGAY' để hệ thống tính toán.")
