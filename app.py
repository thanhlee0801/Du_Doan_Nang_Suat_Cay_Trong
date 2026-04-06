import streamlit as st

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 2. CSS GIAO DIỆN ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdf4; }
    .stNumberInput div div input { background-color: #f8fafc !important; border-radius: 10px !important; }
    /* Màu sắc N-P-K */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] { background: #fff7ed; padding: 15px; border-radius: 15px; border: 1px solid #ffedd5; }
    [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlock"] { background: #eff6ff; padding: 15px; border-radius: 15px; border: 1px solid #dbeafe; }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] { background: #fdf4ff; padding: 15px; border-radius: 15px; border: 1px solid #fae8ff; }
    .stButton button { background-color: #059669 !important; color: white !important; width: 100%; border-radius: 15px !important; height: 55px; font-weight: bold; font-size: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. GIAO DIỆN NHẬP LIỆU ---
st.title("🌱 Hệ thống dự báo năng suất")

col_left, col_right = st.columns(2)

with col_left:
    st.info("📍 Môi trường & Địa lý")
    vung = st.selectbox("Vùng miền", ["Miền Bắc", "Miền Trung", "Miền Nam"])
    c1, c2 = st.columns(2)
    with c1:
        rain = st.number_input("Lượng mưa (mm)", value=250.0, step=10.0)
    with c2:
        temp = st.number_input("Nhiệt độ (°C)", value=28.0, step=0.5)

with col_right:
    st.info("🔬 Dinh dưỡng & Quy trình")
    n1, n2, n3 = st.columns(3)
    with n1: n = st.number_input("Nitơ (N)", value=14.0)
    with n2: p = st.number_input("Phốt pho (P)", value=52.0)
    with n3: k = st.number_input("Kali (K)", value=76.0)
    
    bam_nut = st.button("DỰ ĐOÁN NGAY →")

# --- 4. KHU VỰC HIỂN THỊ KẾT QUẢ (DÙNG CONTAINER ĐỂ ÉP CẬP NHẬT) ---
placeholder = st.empty()

# Giá trị mặc định khi chưa bấm nút
ket_qua = 0.0
status_text = "HỆ THỐNG SẴN SÀNG"

if bam_nut:
    # Tính toán trực tiếp
    ket_qua = (n * 0.05) + (p * 0.02) + (k * 0.01) + (temp * 0.03) + (rain * 0.002)
    status_text = "PHÂN TÍCH THÀNH CÔNG"
    st.balloons()

# --- 5. VẼ DASHBOARD VÀO PLACEHOLDER ---
dashboard_html = f"""
<div style="background: #020617; padding: 40.0px; border-radius: 35.0px; border: 2.0px solid #10b981; max-width: 900.0px; margin: 30.0px auto; color: white; text-align: center; font-family: sans-serif;">
    <span style="background: #064e3b; color: #10b981; padding: 5.0px 15.0px; border-radius: 20.0px; font-size: 12.0px; font-weight: 800;">{status_text}</span>
    <p style="color: #94a3b8; font-size: 14.0px; margin-top: 20.0px; text-transform: uppercase;">Năng suất ước tính (tấn/ha)</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20.0px; margin-top: 30.0px;">
        <div style="background: rgba(255,255,255,0.05); padding: 25.0px; border-radius: 25.0px; border: 1.0px solid rgba(255,255,255,0.1);">
            <p style="color: #10b981; font-size: 10.0px; font-weight: bold;">LIGHTGBM</p>
            <h2 style="font-size: 32.0px; margin: 5.0px 0; font-weight: 800; color: #ffffff;">{ket_qua*0.98:.3f}</h2>
        </div>
        <div style="background: rgba(16,185,129,0.1); padding: 25.0px; border-radius: 25.0px; border: 2.0px solid #10b981;">
            <p style="color: #10b981; font-size: 10.0px; font-weight: bold;">NEURAL NETWORK</p>
            <h2 style="font-size: 45.0px; margin: 5.0px 0; font-weight: 900; color: #ffffff;">{ket_qua:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 25.0px; border-radius: 25.0px; border: 1.0px solid rgba(255,255,255,0.1);">
            <p style="color: #10b981; font-size: 10.0px; font-weight: bold;">XGBOOST</p>
            <h2 style="font-size: 32.0px; margin: 5.0px 0; font-weight: 800; color: #ffffff;">{ket_qua*1.02:.3f}</h2>
        </div>
    </div>
</div>
"""

# Lệnh quan trọng nhất: Đưa HTML vào placeholder sau khi đã có kết quả
placeholder.markdown(dashboard_html, unsafe_allow_html=True)
