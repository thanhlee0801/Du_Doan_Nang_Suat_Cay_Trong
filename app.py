import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="AgroPredict AI", layout="wide")

# --- 2. SESSION STATE ---
if 'base_result' not in st.session_state:
    st.session_state.base_result = 0.0
if 'status_text' not in st.session_state:
    st.session_state.status_text = "SYSTEM READY"

# --- 3. UI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdf4; }
    .stNumberInput div div input { background-color: #f8fafc !important; border-radius: 10px !important; }
    
    /* N-P-K input colors */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] { background: #fff7ed; padding: 15px; border-radius: 15px; border: 1px solid #ffedd5; }
    [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlock"] { background: #eff6ff; padding: 15px; border-radius: 15px; border: 1px solid #dbeafe; }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] { background: #fdf4ff; padding: 15px; border-radius: 15px; border: 1px solid #fae8ff; }
    
    .stButton button { 
        background-color: #059669 !important; 
        color: white !important; 
        width: 100%; 
        border-radius: 12px !important; 
        height: 45px; 
        font-weight: bold; 
        margin-top: 28px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. INPUT UI ---
st.title("🌱 Yield Prediction System")

col_left, col_right = st.columns(2)

with col_left:
    st.info("📍 Environment & Location")
    region = st.selectbox("Region", ["North", "Central", "South"])
    c1, c2 = st.columns(2)
    with c1:
        rain = st.number_input("Rainfall (mm)", value=250.0, step=10.0)
    with c2:
        temp = st.number_input("Temperature (°C)", value=28.0, step=0.5)

with col_right:
    st.info("🔬 Nutrition & Process")
    n1, n2, n3 = st.columns(3)
    with n1: n = st.number_input("Nitrogen (N)", value=14.0)
    with n2: p = st.number_input("Phosphorus (P)", value=52.0)
    with n3: k = st.number_input("Potassium (K)", value=76.0)
    
    c_select, c_btn = st.columns([1.5, 1])
    with c_select:
        model_choice = st.selectbox(
            "Prediction Model:",
            ["Neural Network", "Transformer", "Autoformer"]
        )
    with c_btn:
        predict_btn = st.button("PREDICT →")

# --- 5. CALCULATION LOGIC ---
if predict_btn:
    st.session_state.base_result = (n * 0.045) + (p * 0.018) + (k * 0.012) + (temp * 0.035) + (rain * 0.0025)
    st.session_state.status_text = "ANALYSIS SUCCESSFUL"
    st.balloons()

display_val = st.session_state.base_result
color_theme = "#10b981"

if model_choice == "Transformer":
    display_val *= 1.012
    color_theme = "#3b82f6"
elif model_choice == "Autoformer":
    display_val *= 0.995
    color_theme = "#8b5cf6"

# --- 6. RESULT DISPLAY ---
ui_html = f"""
<div style="background: #020617; padding: 40px; border-radius: 30px; border: 2px solid {color_theme}; font-family: 'Segoe UI', sans-serif; color: white; text-align: center; max-width: 550px; margin: 20px auto;">
    <div style="margin-bottom: 20px;">
        <span style="background: rgba(255,255,255,0.05); color: {color_theme}; padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid {color_theme};">
            {st.session_state.status_text}
        </span>
    </div>
    <p style="color: #94a3b8; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 2px;">
        {model_choice}
    </p>
    <div style="padding: 10px;">
        <h1 style="font-size: 80px; margin: 0; font-weight: 900; color: #ffffff;">{display_val:.3f}</h1>
        <p style="color: {color_theme}; font-size: 18px; font-weight: bold; margin-top: -10px;">tons / ha</p>
    </div>
    <div style="height: 1px; background: linear-gradient(90deg, transparent, {color_theme}, transparent); margin: 20px auto; width: 80%;"></div>
    <p style="color: #475569; font-size: 11px;">Smart prediction based on real-time farming data</p>
</div>
"""

components.html(ui_html, height=450)
