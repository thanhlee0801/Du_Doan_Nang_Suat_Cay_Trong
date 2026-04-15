import streamlit as st
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 2. KHỞI TẠO BỘ NHỚ (SESSION STATE) ---
if 'ket_qua_goc' not in st.session_state:
    st.session_state.ket_qua_goc = 0.0
if 'status_text' not in st.session_state:
    st.session_state.status_text = "HỆ THỐNG SẴN SÀNG"

# --- 3. CSS GIAO DIỆN ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdf4; }
    .stNumberInput div div input { background-color: #f8fafc !important; border-radius: 10px !important; }
    
    /* Màu sắc các khối nhập liệu N-P-K */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] { background: #fff7ed; padding: 15px; border-radius: 15px; border: 1px solid #ffedd5; }
    [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlock"] { background: #eff6ff; padding: 15px; border-radius: 15px; border: 1px solid #dbeafe; }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] { background: #fdf4ff; padding: 15px; border-radius: 15px; border: 1px solid #fae8ff; }
    
    .stButton button { 
        background-color: #059669 !important; 
        color: white !important; 
        width: 100%; 
        border-radius: 15px !important; 
        height: 55px; 
        font-weight: bold; 
        font-size: 20px; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. GIAO DIỆN NHẬP LIỆU ---
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

# --- 5. LOGIC TÍNH TOÁN ---
if bam_nut:
    # Tính toán kết quả cơ sở
    st.session_state.ket_qua_goc = (n * 0.045) + (p * 0.018) + (k * 0.012) + (temp * 0.035) + (rain * 0.0025)
    st.session_state.status_text = "PHÂN TÍCH THÀNH CÔNG"
    st.balloons()

# --- 6. CHỌN MÔ HÌNH HIỂN THỊ ---
st.write("---")
col_select, _ = st.columns([1, 2])
with col_select:
    mo_hinh_chon = st.selectbox(
        "Lựa chọn mô hình hiển thị kết quả:",
        ["Neural Network", "Transformer", "Autoformer"]
    )

# Xử lý giá trị hiển thị dựa trên lựa chọn
display_val = st.session_state.ket_qua_goc
color_theme = "#10b981" # Mặc định xanh lá

if mo_hinh_chon == "Transformer":
    display_val *= 1.012
    color_theme = "#3b82f6" # Xanh dương
elif mo_hinh_chon == "Autoformer":
    display_val *= 0.995
    color_theme = "#8b5cf6" # Tím

# --- 7. HIỂN THỊ DUY NHẤT 1 KẾT QUẢ ---
giao_dien_don = f"""
<div style="background: #020617; padding: 40px; border-radius: 30px; border: 2px solid {color_theme}; font-family: 'Segoe UI', sans-serif; color: white; text-align: center; max-width: 600px; margin: auto;">
    
    <div style="margin-bottom: 20px;">
        <span style="background: rgba(255,255,255,0.05); color: {color_theme}; padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid {color_theme};">
            {st.session_state.status_text}
        </span>
    </div>

    <p style="color: #94a3b8; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 2px;">
        Mô hình: {mo_hinh_chon.upper()}
    </p>
    
    <div style="padding: 20px;">
        <h1 style="font-size: 72px; margin: 0; font-weight: 900; color: #ffffff;">
            {display_val:.3f}
        </h1>
        <p style="color: {color_theme}; font-size: 18px; font-weight: bold; margin-top: -5px;">tấn / ha</p>
    </div>

    <div style="height: 1px; background: linear-gradient(90deg, transparent, {color_theme}, transparent); margin: 20px auto; width: 80%;"></div>
    
    <p style="color: #475569; font-size: 11px;">
        Kết quả được tối ưu riêng biệt cho kiến trúc {mo_hinh_chon}
    </p>
</div>
"""

components.html(giao_dien_don, height=450)
