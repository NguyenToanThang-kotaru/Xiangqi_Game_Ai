import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

# Load dữ liệu đã chia
X_train = pd.read_csv("dataset/X_train.csv")
X_test = pd.read_csv("dataset/X_test.csv")
y_score_train = pd.read_csv("dataset/y_score_train.csv").values.ravel()  # Ravel để đảm bảo y là vector 1D
y_score_test = pd.read_csv("dataset/y_score_test.csv").values.ravel()
y_winrate_train = pd.read_csv("dataset/y_winrate_train.csv").values.ravel()
y_winrate_test = pd.read_csv("dataset/y_winrate_test.csv").values.ravel()

import matplotlib.pyplot as plt

plt.hist(y_score_train, bins=50, edgecolor="black")
plt.xlabel("Score")
plt.ylabel("Số lượng")
plt.title("Phân bố Score trước khi phân loại")
plt.show()
# Chuyển `score` thành nhãn phân loại
bins = [-float('inf'), -1000, -400, -100, -1, 0, 1, 100, 400, 1000, float('inf')]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8]

y_score_train = np.digitize(y_score_train, bins=bins, right=True) - 1
print("Giá trị score trước khi phân loại:", y_score_train[:10])

# print(" Giá trị score sau khi phân loại:", np.digitize(y_score_train[:10].values.ravel(), bins=bins, right=True) - 1)
y_score_test = np.digitize(y_score_test, bins=bins, right=True) - 1

# 🔥 Khởi tạo mô hình Random Forest
model_score = RandomForestClassifier(n_estimators=100, random_state=42)  # Phân loại score
model_winrate = RandomForestRegressor(n_estimators=100, random_state=42)  # Hồi quy winrate

# 🚀 Huấn luyện mô hình Score
print("Đang huấn luyện mô hình Random Forest cho Score...")
model_score.fit(X_train, y_score_train)

# 🚀 Huấn luyện mô hình Winrate
print("Đang huấn luyện mô hình Random Forest cho Winrate...")
model_winrate.fit(X_train, y_winrate_train)

# 📊 Đánh giá mô hình Score
y_score_pred = model_score.predict(X_test)
accuracy = accuracy_score(y_score_test, y_score_pred)
print(f"Độ chính xác của mô hình Score: {accuracy * 100:.2f}%")

# 📊 Đánh giá mô hình Winrate
y_winrate_pred = model_winrate.predict(X_test)
mse = mean_squared_error(y_winrate_test, y_winrate_pred)
print(f"Lỗi trung bình bình phương (MSE) của mô hình Winrate: {mse:.4f}")
from sklearn.metrics import classification_report
print(classification_report(y_score_test, y_score_pred))
# 💾 Lưu mô hình đã huấn luyện
joblib.dump(model_score, "ai/random_forest_score.pkl")
joblib.dump(model_winrate, "ai/random_forest_winrate.pkl")
print("Mô hình đã được lưu vào ai/random_forest_score.pkl và ai/random_forest_winrate.pkl!")
