import streamlit as st
import pandas as pd
import joblib
import os

# Cấu hình trang
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 1. LOAD MODELS ---
# Đường dẫn tới thư mục chứa model (thay đổi tùy theo cấu trúc máy bạn)
MODEL_PATH = "Du_Doan_Nang_Suat_Cay_Trong-main/backend/model/"

@st.cache_resource
def load_all_models():
    models = {}
    try:
        models['rf'] = joblib.load(os.path.join(MODEL_PATH, "random_forest_model.pkl"))
        models['xgb'] = joblib.load(os.path.join(MODEL_PATH, "xgboost_model.pkl"))
        models['lgbm'] = joblib.load(os.path.join(MODEL_PATH, "lightgbm_model.pkl"))
        # Thêm các model khác nếu có trong thư mục của bạn
    except Exception as e:
        st.error(f"Lỗi load model: {e}")
    return models

models = load_all_models()

# --- 2. GIAO DIỆN (FRONTEND) ---
st.markdown("""
    <style>
    .main { background-color: #f0fdf4; }
    .stButton>button { width: 100%; background-color: #10b981; color: white; border-radius: 12px; height: 3em; font-weight: bold; }
    .result-card { background: linear-gradient(135deg, #064e3b 0%, #020617 100%); color: white; padding: 20px; border-radius: 20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("AgroPredict AI 🌾")
st.write("Dự đoán năng suất dựa trên dữ liệu thổ nhưỡng")

# Chia cột nhập liệu
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Môi trường & Địa lý")
    region = st.selectbox("Vùng miền", ["Miền Bắc", "Miền Trung", "Miền Nam"])
    soil_type = st.selectbox("Loại đất", ["Đất Cát", "Đất Phù Sa", "Đất Phèn"])
    crop = st.selectbox("Cây trồng", ["Lúa", "Ngô", "Khoai"])
    rainfall = st.number_input("Lượng mưa (mm)", value=250)
    temp = st.number_input("Nhiệt độ (°C)", value=28)

with col2:
    st.subheader("🧪 Dinh dưỡng & Quy trình")
    n = st.number_input("Nitơ (N)", value=14)
    p = st.number_input("Phốt pho (P)", value=52)
    k = st.number_input("Kali (K)", value=76)
    weather = st.radio("Thời tiết", ["Nắng", "Mưa", "Âm u"], horizontal=True)
    harvest_days = st.number_input("Ngày thu hoạch dự kiến", value=72)

# --- 3. LOGIC DỰ ĐOÁN ---
if st.button("DỰ ĐOÁN NGAY →"):
    # Chuẩn bị dữ liệu đầu vào (Lưu ý: Tên cột phải khớp chính xác với lúc bạn Train Model)
    # Ở đây tôi ví dụ 5 cột cơ bản, bạn cần điều chỉnh theo đúng file training của bạn
    input_df = pd.DataFrame([[n, p, k, temp, rainfall]], 
                            columns=['N', 'P', 'K', 'temperature', 'rainfall'])
    
    # Thực hiện dự đoán
    res_rf = models['rf'].predict(input_df)[0] if 'rf' in models else 0
    res_xgb = models['xgb'].predict(input_df)[0] if 'xgb' in models else 0
    res_lgbm = models['lgbm'].predict(input_df)[0] if 'lgbm' in models else 0

    # --- 4. HIỂN THỊ KẾT QUẢ ---
    st.markdown("---")
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.write("### NĂNG SUẤT ƯỚC TÍNH")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Random Forest", f"{res_rf:.3f} tấn/ha")
    res_col2.metric("XGBoost", f"{res_xgb:.3f} tấn/ha")
    res_col3.metric("LightGBM", f"{res_lgbm:.3f} tấn/ha")
    
    st.markdown('</div>', unsafe_allow_html=True)
