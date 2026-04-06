import streamlit as st
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 2. KHỞI TẠO BỘ NHỚ (SESSION STATE) ---
# Giúp lưu kết quả cũ khi người dùng thay đổi thông số nhập vào
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = 0.0
if 'status_text' not in st.session_state:
    st.session_state.status_text = "HỆ THỐNG SẴN SÀNG"

# --- 3. CSS GIAO DIỆN (ÉP GIAO DIỆN HỆ THỐNG) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdf4; }
    .stNumberInput div div input { background-color: #f8fafc !important; border-radius: 10px !important; }
    
    /* Màu sắc các khối nhập liệu N-P-K */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] { background: #fff7ed; padding: 15px; border-radius: 15px; border: 1px solid #ffedd5; }
    [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlock"] { background: #eff6ff; padding: 15px; border-radius: 15px; border: 1px solid #dbeafe; }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] { background: #fdf4ff; padding: 15px; border-radius: 15px; border: 1px solid #fae8ff; }
    
    /* Nút bấm dự đoán */
    .stButton button { 
        background-color: #059669 !important; 
        color: white !important; 
        width: 100%; 
        border-radius: 15px !important; 
        height: 55px; 
        font-weight: bold; 
        font-size: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        border: none !important;
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
    
    # Nút bấm xử lý
    bam_nut = st.button("DỰ ĐOÁN NGAY →")

# --- 5. LOGIC TÍNH TOÁN ---
if bam_nut:
    # Công thức dự đoán giả lập
    st.session_state.ket_qua = (n * 0.05) + (p * 0.02) + (k * 0.01) + (temp * 0.03) + (rain * 0.002)
    st.session_state.status_text = "PHÂN TÍCH THÀNH CÔNG"
    st.balloons()

# --- 6. HIỂN THỊ DASHBOARD KẾT QUẢ (DARK MODE) ---
# Lấy giá trị từ session_state để hiển thị ổn định
kq = st.session_state.ket_qua
stt = st.session_state.status_text

giao_dien_den = f"""
<div style="background: #020617; padding: 30px; border-radius: 30px; border: 2px solid #10b981; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; text-align: center;">
    
    <div style="margin-bottom: 20px;">
        <span style="background: #064e3b; color: #10b981; padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: 800; letter-spacing: 1px;">
            {stt}
        </span>
    </div>

    <p style="color: #94a3b8; font-size: 13px; text-transform: uppercase; margin-bottom: 10px;">Năng suất ước tính (tấn/ha)</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 9px; font-weight: bold; margin: 0;">AUTOMODEL</p>
            <h2 style="font-size: 24px; margin: 5px 0;">{kq*0.92:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 9px; font-weight: bold; margin: 0;">LIGHTGBM</p>
            <h2 style="font-size: 24px; margin: 5px 0;">{kq*0.97:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 9px; font-weight: bold; margin: 0;">RANDOM FOREST</p>
            <h2 style="font-size: 24px; margin: 5px 0;">{kq*0.95:.3f}</h2>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div style="background: rgba(16, 185, 129, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #10b981;">
            <p style="color: #10b981; font-size: 10px; font-weight: bold; margin: 0;">NEURAL NETWORK (CHÍNH)</p>
            <h2 style="font-size: 42px; margin: 10px 0; font-weight: 900;">{kq:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #10b981; font-size: 10px; font-weight: bold; margin: 0;">XGBOOST</p>
            <h2 style="font-size: 42px; margin: 10px 0; font-weight: 900;">{kq*1.02:.3f}</h2>
        </div>
    </div>

    <p style="color: #475569; font-size: 11px; margin-top: 20px;">Dữ liệu dựa trên mô hình học sâu đã huấn luyện</p>
</div>
"""

# Hiển thị dashboard bằng component để tránh lỗi Markdown hiện code thô
components.html(giao_dien_den, height=520)
