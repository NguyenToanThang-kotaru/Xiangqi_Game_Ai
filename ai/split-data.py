import pandas as pd
from sklearn.model_selection import train_test_split

# 📂 Load dữ liệu đã tiền xử lý
df = pd.read_csv("dataset/processed_data_cleaned.csv")

# 🏷 Xác định đặc trưng (X) và nhãn (y)
X = df.iloc[:, :-2]  # Loại bỏ 2 cột cuối (score, winrate)
y_score = df.iloc[:, -2]  # Cột score
y_winrate = df.iloc[:, -1]  # Cột winrate

print("📊 X columns:", X.columns)
print("📊 y column (score):", y_score.name)
print("📊 y column (winrate):", y_winrate.name)

# ✂️ Chia thành tập train (70%) và test (30%)
X_train, X_test, y_score_train, y_score_test = train_test_split(X, y_score, test_size=0.3, random_state=42)
X_train, X_test, y_winrate_train, y_winrate_test = train_test_split(X, y_winrate, test_size=0.3, random_state=42)



# 📝 Kiểm tra kích thước tập dữ liệu
print(f"📊 Số lượng mẫu train: {X_train.shape[0]}")
print(f"📊 Số lượng mẫu test: {X_test.shape[0]}")
print(f"📊 Số lượng cột X: {X.shape[1]}")

# 🏷 Xuất ra file để kiểm tra lại
X_train.to_csv("dataset/X_train.csv", index=False)
X_test.to_csv("dataset/X_test.csv", index=False)
y_score_train.to_csv("dataset/y_score_train.csv", index=False)
y_score_test.to_csv("dataset/y_score_test.csv", index=False)
y_winrate_train.to_csv("dataset/y_winrate_train.csv", index=False)
y_winrate_test.to_csv("dataset/y_winrate_test.csv", index=False)

print("✅ Đã chia dữ liệu và lưu vào file X_train.csv, X_test.csv, y_score_train.csv, y_score_test.csv, y_winrate_train.csv, y_winrate_test.csv!")

# 🔍 Kiểm tra dữ liệu có bị thiếu không
missing_values = df.isnull().sum().sum()
print(f"🔍 Tổng số giá trị bị thiếu: {missing_values}")  # Nếu != 0 thì có giá trị bị thiếu