import streamlit as st
import streamlit.components.v1 as components
import os

# Đường dẫn tới file index.html nằm TRONG thư mục dist
# (Điều chỉnh lại tên thư mục cho đúng với cấu trúc GitHub của bạn)
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, "Du_Doan_Nang_Suat_Cay_Trong-main", "frontend", "dist", "index.html")

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    # Render giao diện React đã build
    components.html(html_data, height=1000, scrolling=True)
else:
    st.error(f"Không tìm thấy file tại: {html_path}")
    # Nếu lỗi, dòng này sẽ giúp bạn debug cấu trúc thư mục
    st.write("Cấu trúc hiện tại:", os.listdir(current_dir))
