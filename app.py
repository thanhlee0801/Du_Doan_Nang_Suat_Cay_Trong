import streamlit as st
import streamlit.components.v1 as components
import os

# Cấu hình trang (tùy chọn)
st.set_page_config(page_title="My Web App", layout="wide")

# Đường dẫn đến file HTML
frontend_path = os.path.join("frontend", "index.html")

# Đọc nội dung file HTML
with open(frontend_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Hiển thị HTML lên Streamlit
# Bạn có thể điều chỉnh width và height cho phù hợp với giao diện
components.html(html_content, height=800, scrolling=True)
