import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 📂 Load dữ liệu đã chia
X_train = pd.read_csv("dataset/X_train.csv")
X_test = pd.read_csv("dataset/X_test.csv")
y_train = pd.read_csv("dataset/y_train.csv").values.ravel()  # Ravel để đảm bảo y là vector 1D
y_test = pd.read_csv("dataset/y_test.csv").values.ravel()

# 🔄 Chuyển `score` thành nhãn phân loại
bins = [-float('inf'), -500, 500, float('inf')]  # Ngưỡng phân loại
labels = [0, 1, 2]  # 0: kém, 1: trung bình, 2: tốt

y_train = np.digitize(y_train, bins=bins, right=True) - 1
y_test = np.digitize(y_test, bins=bins, right=True) - 1

# 🔥 Khởi tạo mô hình Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 🚀 Huấn luyện mô hình
print("🚀 Đang huấn luyện mô hình Random Forest...")
model.fit(X_train, y_train)

# 📊 Đánh giá mô hình
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Độ chính xác của mô hình: {accuracy * 100:.2f}%")

# 💾 Lưu mô hình đã huấn luyện
joblib.dump(model, "ai/random_forest_model.pkl")
print("📁 Mô hình đã được lưu vào ai/random_forest_model.pkl!")
