import pandas as pd
from sklearn.model_selection import train_test_split

# 📂 Load dữ liệu đã tiền xử lý
df = pd.read_csv("processed_data_cleaned.csv")

# 🏷 Xác định đặc trưng (X) và nhãn (y)
X = df.iloc[:, :-2]  # Tất cả cột trừ 2 cột cuối (score, winrate)
y = df.iloc[:, -2]   # Cột score (hoặc có thể dùng winrate)

# ✂️ Chia thành tập train (70%) và test (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 📝 Kiểm tra kích thước tập dữ liệu
print(f"📊 Số lượng mẫu train: {X_train.shape[0]}")
print(f"📊 Số lượng mẫu test: {X_test.shape[0]}")

# 🏷 Xuất ra file để kiểm tra lại
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("✅ Đã chia dữ liệu và lưu vào file X_train.csv, X_test.csv, y_train.csv, y_test.csv!")
