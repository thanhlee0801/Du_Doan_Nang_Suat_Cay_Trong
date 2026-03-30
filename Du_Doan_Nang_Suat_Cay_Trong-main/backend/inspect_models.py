import joblib
from tensorflow.keras.models import load_model
import numpy as np

# === 1. MỞ VÀ XEM MÔ HÌNH KERAS ===
print("===== MÔ HÌNH NEURAL NETWORK (.keras) =====")
try:
    keras_model = load_model('model/neural_network_model.keras')
    keras_model.summary()

    for i, layer in enumerate(keras_model.layers):
        weights, biases = layer.get_weights()
        print(f"\n🔹 Lớp {i} - {layer.name}")
        print(f"  Trọng số: {weights.shape}")
        print(f"  Bias: {biases.shape}")
except Exception as e:
    print("Lỗi khi mở file .keras:", e)

# === 2. MỞ VÀ XEM MÔ HÌNH RANDOM FOREST (.pkl) ===
print("\n===== MÔ HÌNH RANDOM FOREST (.pkl) =====")
try:
    rf_model = joblib.load('model/random_forest_model.pkl')
    print(rf_model)
except Exception as e:
    print("Lỗi khi mở random_forest_model.pkl:", e)

# === 3. MỞ SCALER ===
print("\n===== SCALER (.pkl) =====")
try:
    scaler = joblib.load('model/scaler.pkl')
    print("Mean:", scaler.mean_)
    print("Scale:", scaler.scale_)
except Exception as e:
    print("Lỗi khi mở scaler.pkl:", e)

# === 4. MỞ ENCODER CHO REGION (VD) ===
print("\n===== LABEL ENCODER: Region =====")
try:
    le_region = joblib.load('model/label_encoder_Region.pkl')
    print("Các lớp (classes_):", le_region.classes_)
except Exception as e:
    print("Lỗi khi mở label_encoder_Region.pkl:", e)
