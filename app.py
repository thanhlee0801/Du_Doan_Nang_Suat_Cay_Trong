import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# Phần CSS và HTML giao diện
# Lưu ý: Sử dụng Tailwind CSS qua CDN để đảm bảo style giống hệt ảnh
html_code = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { 
        font-family: 'Inter', sans-serif; 
        background-color: #f0fdf4; 
        margin: 0;
        display: flex;
        justify-content: center;
        padding: 20px;
    }
    .card-shadow { box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05); }
    .gradient-bg { background: linear-gradient(135deg, #064e3b 0%, #020617 100%); }
    .input-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; width: 100%; font-size: 14px; outline: none; }
    input:focus, select:focus { border-color: #10b981; ring: 2px; ring-color: #10b981; }
  </style>
</head>
<body>
  <div style="max-width: 1000px; width: 100%;">
    <header style="text-align: center; margin-bottom: 40px;">
      <h1 style="font-size: 36px; font-weight: 800; color: #1e293b; margin-bottom: 8px;">
        AgroPredict <span style="color: #10b981;">AI</span>
      </h1>
      <p style="color: #64748b; font-size: 14px; max-width: 500px; margin: 0 auto; line-height: 1.6;">
        Ứng dụng công nghệ học máy để tối ưu hóa năng suất nông nghiệp dựa trên dữ liệu thổ nhưỡng và khí hậu.
      </p>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-bottom: 30px;">
      
      <div style="background: white; border-radius: 32px; padding: 30px; border: 1px solid white;" class="card-shadow">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            <div style="background: #ecfdf5; padding: 10px; border-radius: 12px; color: #059669;">📍</div>
            <div>
                <h3 style="font-weight: 700; color: #1e293b; margin: 0;">Môi trường & Địa lý</h3>
                <p style="font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin: 0;">Thông tin vùng miền và khí hậu</p>
            </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div>
                <label style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-left: 4px;">Vùng miền canh tác</label>
                <select class="input-box"><option>Miền Bắc</option></select>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <label style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Loại đất</label>
                    <select class="input-box"><option>Đất Cát</option></select>
                </div>
                <div>
                    <label style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Cây trồng</label>
                    <select class="input-box"><option>Lúa</option></select>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <label style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Lượng mưa (mm)</label>
                    <input type="number" class="input-box" value="250">
                </div>
                <div>
                    <label style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Nhiệt độ (°C)</label>
                    <input type="number" class="input-box" value="28">
                </div>
            </div>
        </div>
      </div>

      <div style="background: white; border-radius: 32px; padding: 30px; border: 1px solid white; display: flex; flex-direction: column; justify-content: space-between;" class="card-shadow">
        <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="background: #eff6ff; padding: 10px; border-radius: 12px; color: #2563eb;">🧪</div>
                <div>
                    <h3 style="font-weight: 700; color: #1e293b; margin: 0;">Dinh dưỡng & Quy trình</h3>
                    <p style="font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin: 0;">Thông số hóa lý và thời gian</p>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
                <div style="background: #fffaf5; border: 1px solid #ffedd5; padding: 15px; border-radius: 16px; text-align: center;">
                    <span style="font-size: 9px; font-weight: 900; color: #fb923c; display: block;">NITƠ (N)</span>
                    <span style="font-size: 24px; font-weight: 700; color: #ea580c;">14</span>
                </div>
                <div style="background: #f0f7ff; border: 1px solid #dbeafe; padding: 15px; border-radius: 16px; text-align: center;">
                    <span style="font-size: 9px; font-weight: 900; color: #60a5fa; display: block;">P (P)</span>
                    <span style="font-size: 24px; font-weight: 700; color: #2563eb;">52</span>
                </div>
                <div style="background: #faf5ff; border: 1px solid #f3e8ff; padding: 15px; border-radius: 16px; text-align: center;">
                    <span style="font-size: 9px; font-weight: 900; color: #c084fc; display: block;">KALI (K)</span>
                    <span style="font-size: 24px; font-weight: 700; color: #9333ea;">76</span>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="font-size: 10px; font-weight: 700; text-align: center; color: #94a3b8; text-transform: uppercase; margin-bottom: 10px;">Thời tiết hiện tại</p>
                <div style="display: flex; background: #f1f5f9; padding: 4px; border-radius: 12px;">
                    <button style="flex: 1; padding: 8px; background: white; border-radius: 8px; font-size: 12px; font-weight: 700; border: none; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">Nắng</button>
                    <button style="flex: 1; padding: 8px; background: transparent; color: #94a3b8; border: none; font-size: 12px;">Mưa</button>
                    <button style="flex: 1; padding: 8px; background: transparent; color: #94a3b8; border: none; font-size: 12px;">Âm u</button>
                </div>
            </div>
        </div>

        <button style="width: 100%; background: #059669; color: white; border: none; padding: 15px; border-radius: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 8px; box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);">
            DỰ ĐOÁN NGAY <span>→</span>
        </button>
      </div>
    </div>

    <div class="gradient-bg" style="border-radius: 32px; padding: 40px; text-align: center; position: relative; color: white;">
        <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #10b981; font-size: 10px; font-weight: 900; padding: 6px 16px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px;">
            Phân tích thành công
        </div>
        <p style="font-size: 11px; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; margin-top: 10px;">Năng suất ước tính từ các mô hình</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 20px;">
            <div>
                <p style="font-size: 9px; color: #10b981; font-weight: 700; text-transform: uppercase;">Transformer</p>
                <p style="font-size: 24px; font-weight: 700;">2.49 <small style="font-size: 10px; color: #64748b; font-weight: 400;">tấn/ha</small></p>
            </div>
            <div>
                <p style="font-size: 9px; color: #10b981; font-weight: 700; text-transform: uppercase;">LightGBM</p>
                <p style="font-size: 24px; font-weight: 700;">2.629 <small style="font-size: 10px; color: #64748b; font-weight: 400;">tấn/ha</small></p>
            </div>
            <div>
                <p style="font-size: 9px; color: #10b981; font-weight: 700; text-transform: uppercase;">Neural Net</p>
                <p style="font-size: 24px; font-weight: 700;">2.545 <small style="font-size: 10px; color: #64748b; font-weight: 400;">tấn/ha</small></p>
            </div>
            <div>
                <p style="font-size: 9px; color: #10b981; font-weight: 700; text-transform: uppercase;">XGBoost</p>
                <p style="font-size: 24px; font-weight: 700;">2.658 <small style="font-size: 10px; color: #64748b; font-weight: 400;">tấn/ha</small></p>
            </div>
        </div>
    </div>
  </div>
</body>
</html>
"""

# Hiển thị vào Streamlit
components.html(html_code, height=900, scrolling=True)
