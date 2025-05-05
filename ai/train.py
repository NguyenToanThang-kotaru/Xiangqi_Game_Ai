import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error

# Load dữ liệu huấn luyện đầu vào + đầu ra
X_train = pd.read_csv("dataset/X_train.csv")   # 92 cột: fen_array (910 + turn (1) + winrate (1)
X_test = pd.read_csv("dataset/X_test.csv")

y_train = pd.read_csv("dataset/y_move_train.csv")   # 4 cột: move vector
y_test = pd.read_csv("dataset/y_move_test.csv")

# 🚀 Huấn luyện mô hình MultiOutput Random Forest cho Move Prediction
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# 📊 Dự đoán
y_pred = model.predict(X_test)

# 📉 Đánh giá bằng lỗi trung bình bình phương
mse = mean_squared_error(y_test, y_pred)
print(f"🎯 MSE của mô hình dự đoán nước đi: {mse:.4f}")

# 💾 Lưu mô hình
joblib.dump(model, "ai/random_forest_move_predictor.pkl")
print("✅ Đã lưu mô hình dự đoán nước đi vào ai/random_forest_move_predictor.pkl")
