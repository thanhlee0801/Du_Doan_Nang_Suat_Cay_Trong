import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide")

# Lấy thư mục gốc của project trên Streamlit Cloud
base_path = os.path.dirname(os.path.abspath(__file__))

# Thử các đường dẫn có thể xảy ra
possible_paths = [
    os.path.join(base_path, "frontend", "dist", "index.html"),
    os.path.join(base_path, "Du_Doan_Nang_Suat_Cay_Trong-main", "frontend", "dist", "index.html"),
]

html_content = None
for path in possible_paths:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        break

if html_content:
    # Tăng height lên để tránh trang trắng do iframe quá ngắn
    components.html(html_content, height=1200, scrolling=True)
else:
    st.error("Vẫn không tìm thấy thư mục 'dist' trên GitHub!")
    st.write("Cấu trúc thư mục hiện tại trên server:")
    # Liệt kê file để debug
    for root, dirs, files in os.walk(base_path):
        if 'node_modules' in dirs: dirs.remove('node_modules') # Bỏ qua thư mục rác
        level = root.replace(base_path, '').count(os.sep)
        st.code(f"{' ' * 4 * level}{os.path.basename(root)}/")
