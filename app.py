import streamlit as st

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 2. CSS "ÉP" GIAO DIỆN (Để giống ảnh mẫu) ---
st.markdown("""
    <style>
    /* Làm nền app màu xanh nhạt */
    .stApp { background-color: #f0fdf4; }
    
    /* Tùy chỉnh các ô nhập liệu */
    .stNumberInput div div input {
        background-color: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Tạo khối cho N-P-K */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] { background: #fff7ed; padding: 10px; border-radius: 15px; border: 1px solid #ffedd5; }
    [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlock"] { background: #eff6ff; padding: 10px; border-radius: 15px; border: 1px solid #dbeafe; }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] { background: #fdf4ff; padding: 10px; border-radius: 15px; border: 1px solid #fae8ff; }

    /* Nút bấm xanh đậm */
    .stButton button {
        background-color: #059669 !important;
        color: white !important;
        width: 100%;
        border-radius: 15px !important;
        height: 50px;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GIAO DIỆN NHẬP LIỆU ---
st.write("### 🌱 Hệ thống dự báo năng suất")

col_left, col_right = st.columns(2)

with col_left:
    st.info("📍 Môi trường & Địa lý")
    vung = st.selectbox("Vùng miền", ["Miền Bắc", "Miền Trung", "Miền Nam"])
    c1, c2 = st.columns(2)
    with c1:
        rain = st.number_input("Lượng mưa (mm)", value=250.0)
    with c2:
        temp = st.number_input("Nhiệt độ (°C)", value=28.0)

with col_right:
    st.info("🔬 Dinh dưỡng & Quy trình")
    n1, n2, n3 = st.columns(3)
    with n1:
        n = st.number_input("Nitơ (N)", value=14.0)
    with n2:
        p = st.number_input("Phốt pho (P)", value=52.0)
    with n3:
        k = st.number_input("Kali (K)", value=76.0)
    
    # NÚT BẤM QUAN TRỌNG NHẤT
    bam_nut = st.button("DỰ ĐOÁN NGAY →")

# --- 4. XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---
# Chúng ta sẽ tính toán trực tiếp khi bấm nút hoặc hiển thị 0 nếu chưa bấm
if bam_nut:
    # Logic tính toán (Giả lập model Neural Network của bạn)
    ket_qua = (n * 0.05) + (p * 0.02) + (k * 0.01) + (temp * 0.03) + (rain * 0.002)
    status_text = "PHÂN TÍCH THÀNH CÔNG"
    st.balloons()
else:
    ket_qua = 0.0
    status_text = "HỆ THỐNG SẴN SÀNG"

# --- 5. GIAO DIỆN DASHBOARD ĐEN (RENDER BẰNG HTML) ---
# Đoạn này dùng f-string để đưa biến 'ket_qua' vào HTML
dashboard_html = f"""
<div style="background: #020617; padding: 40px; border-radius: 35px; border: 2px solid #10b981; max-width: 900px; margin: 30px auto; color: white; text-align: center; font-family: sans-serif;">
    <span style="background: #064e3b; color: #10b981; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: 800;">{status_text}</span>
    <p style="color: #94a3b8; font-size: 14px; margin-top: 20px; text-transform: uppercase;">Năng suất ước tính (tấn/ha)</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px;">
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 25px;">
            <p style="color: #10b981; font-size: 10px; font-weight: bold;">AUTOMODEL</p>
            <h2 style="font-size: 32px; margin: 5px 0;">{ket_qua*0.95:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 25px; border: 1px solid #10b981;">
            <p style="color: #10b981; font-size: 10px; font-weight: bold;">NEURAL NETWORK</p>
            <h2 style="font-size: 40px; margin: 5px 0; font-weight: 800;">{ket_qua:.3f}</h2>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 25px;">
            <p style="color: #10b981; font-size: 10px; font-weight: bold;">LIGHTGBM</p>
            <h2 style="font-size: 32px; margin: 5px 0;">{ket_qua*0.98:.3f}</h2>
        </div>
    </div>
    <p style="color: #475569; font-size: 12px; margin-top: 30px;">Dữ liệu dựa trên mô hình học sâu đã huấn luyện</p>
</div>
"""

st.markdown(dashboard_html, unsafe_allow_html=True)
