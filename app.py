import streamlit as st
import streamlit.components.v1 as components
import os

# Lấy đường dẫn tuyệt đối đến thư mục đang chứa file app.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn đến file index.html bên trong thư mục frontend
frontend_path = os.path.join(current_dir, "frontend", "index.html")

# Kiểm tra xem file có thực sự tồn tại không trước khi mở
if os.path.exists(frontend_path):
    with open(frontend_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=800, scrolling=True)
else:
    st.error(f"Không tìm thấy file tại: {frontend_path}")
    # In ra danh sách file để bạn dễ debug
    st.write("Danh sách file hiện có:", os.listdir(current_dir))
