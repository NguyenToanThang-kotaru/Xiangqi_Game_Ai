import pandas as pd
from sklearn.model_selection import train_test_split

# 📂 Load dữ liệu đã tiền xử lý
df = pd.read_csv("dataset/processed_data_cleaned.csv")

# 📊 Tổng số cột trong dataset
total_columns = df.shape[1]

# 🏷 Xác định đặc trưng (X) và nhãn (y_move)
X = df.iloc[:, :-1]  # Bỏ 4 cột cuối (move_vector)
y_move = df.iloc[:, -1]  # 4 cột cuối là nhãn (move vector)

print("📊 X columns:", X.columns)
print("📊 y columns (move vector):", y_move.name)

# ✂️ Chia thành tập train (70%) và test (30%)
X_train, X_test, y_move_train, y_move_test = train_test_split(X, y_move, test_size=0.3, random_state=42)

# 📝 Kiểm tra kích thước tập dữ liệu
print(f"📊 Số lượng mẫu train: {X_train.shape[0]}")
print(f"📊 Số lượng mẫu test: {X_test.shape[0]}")
print(f"📊 Số lượng cột X (đặc trưng): {X.shape[1]}")
print(f"📊 Số lượng cột y (move_vector): {y_move.shape[0]}")

# 🏷 Xuất ra file để kiểm tra lại
X_train.to_csv("dataset/X_train.csv", index=False)
X_test.to_csv("dataset/X_test.csv", index=False)
y_move_train.to_csv("dataset/y_move_train.csv", index=False)
y_move_test.to_csv("dataset/y_move_test.csv", index=False)

print("✅ Đã chia dữ liệu và lưu vào các file train/test!")

# 🔍 Kiểm tra dữ liệu có bị thiếu không
missing_values = df.isnull().sum().sum()
print(f"🔍 Tổng số giá trị bị thiếu: {missing_values}")
