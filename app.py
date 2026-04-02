import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Cấu hình giao diện Streamlit (ẩn menu và padding thừa)
st.set_page_config(page_title="Dự Đoán Năng Suất", layout="wide")

# 2. Xác định đường dẫn tuyệt đối
# Streamlit Cloud thường mount code tại /mount/src/tên-repo/
base_path = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn cụ thể dựa trên cấu trúc bạn cung cấp
frontend_dir = os.path.join(base_path, "Du_Doan_Nang_Suat_Cay_Trong-main", "frontend")
html_path = os.path.join(frontend_dir, "index.html")

# 3. Kiểm tra và hiển thị
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Hiển thị HTML
    # Bạn có thể tăng height lên 1000 hoặc hơn tùy độ dài trang web của bạn
    components.html(html_content, height=1000, scrolling=True)
else:
    st.error("❌ Không tìm thấy file index.html!")
    st.info(f"Đường dẫn đang thử: {html_path}")
    
    # Debug: Liệt kê các thư mục đang có để bạn thấy cấu trúc thực tế
    st.write("Cấu trúc thư mục hiện tại:")
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        st.code(f"{indent}{os.path.basename(root)}/")
