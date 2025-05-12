from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import joblib

# # Hàm tính MSE
# def mean_squared_error(y_true, y_pred):
#     return np.mean((y_true - y_pred) ** 2)

# # Hàm chia dữ liệu theo ngưỡng phân chia
# def split_data(X, y, feature_index, threshold):
#     left_mask = X[:, feature_index] <= threshold
#     right_mask = X[:, feature_index] > threshold
#     left_X, right_X = X[left_mask], X[right_mask]
#     left_y, right_y = y[left_mask], y[right_mask]
    
#     # Kiểm tra nếu nhóm bị trống
#     if len(left_y) == 0 or len(right_y) == 0:
#         return None, None, None, None
    
#     return left_X, right_X, left_y, right_y

# # Hàm xây dựng cây quyết định
# def build_decision_tree(X, y, max_depth=3, depth=0):
#     n_samples, n_features = X.shape
#     if depth >= max_depth or n_samples <= 1:
#         return np.mean(y)  # Trả về giá trị trung bình của nhãn trong nhóm
    
#     best_mse = float('inf')
#     best_split = None
    
#     # Duyệt qua tất cả các đặc trưng và các ngưỡng phân chia
#     for feature_index in range(X.shape[1]):  # Duyệt qua các đặc trưng
#         thresholds = np.unique(X[:, feature_index])  # Các ngưỡng có thể
#         for threshold in thresholds:
#             # Chia dữ liệu theo ngưỡng
#             left_X, right_X, left_y, right_y = split_data(X, y, feature_index, threshold)
#             if left_X is None:  # Nếu nhóm con rỗng, bỏ qua
#                 continue
#             # Tính MSE cho phân chia này
#             mse = (mean_squared_error(left_y, np.mean(left_y)) * len(left_y) +
#                    mean_squared_error(right_y, np.mean(right_y)) * len(right_y)) / len(y)
#             if mse < best_mse:
#                 best_mse = mse
#                 best_split = (feature_index, threshold)
#                 best_left_y = left_y
#                 best_right_y = right_y
    
#     # Phân chia dữ liệu và xây dựng các nhánh con
#     if best_split is None:
#         return np.mean(y)  # Không tìm thấy ngưỡng, trả về trung bình

#     left_X, right_X, left_y, right_y = split_data(X, y, best_split[0], best_split[1])

#     left_node = build_decision_tree(left_X, left_y, max_depth, depth + 1)
#     right_node = build_decision_tree(right_X, right_y, max_depth, depth + 1)

#     return {"split_feature": best_split[0], "threshold": best_split[1], 
#             "left": left_node, "right": right_node}

# # Hàm dự đoán với cây quyết định
# def predict_decision_tree(tree, X):
#     if not isinstance(tree, dict):
#         return tree  # Trả về giá trị dự đoán nếu đã tới lá
#     if X[tree["split_feature"]] <= tree["threshold"]:
#         return predict_decision_tree(tree["left"], X)
#     else:
#         return predict_decision_tree(tree["right"], X)

# # Huấn luyện Random Forest
# def train_random_forest(X, y, n_trees=100, max_depth=3):
#     trees = []
#     n_samples = len(X)
#     for _ in range(n_trees):
#         # Sử dụng bootstrap sampling (mẫu ngẫu nhiên có lặp lại)
#         sample_indices = np.random.choice(n_samples, size=n_samples, replace=True)
#         X_sample = X[sample_indices]
#         y_sample = y[sample_indices]
#         tree = build_decision_tree(X_sample, y_sample, max_depth)
#         trees.append(tree)
#     return trees

# # Dự đoán với Random Forest
# def predict_random_forest(trees, X):
#     predictions = np.array([predict_decision_tree(tree, x) for tree in trees for x in X])
#     # Trả về trung bình cộng của tất cả các dự đoán từ các cây
#     return np.mean(predictions, axis=0)

# # Tiền xử lý dữ liệu và chia dữ liệu train/test (nếu chưa chia)
# X_train = pd.read_csv("dataset/X_train.csv")   # 92 cột: fen_array (910 + turn (1) + winrate (1)
# X_test = pd.read_csv("dataset/X_test.csv")

# y_train = pd.read_csv("dataset/y_move_train.csv")   # 4 cột: move vector
# y_test = pd.read_csv("dataset/y_move_test.csv")

# # Huấn luyện mô hình Random Forest
# n_trees = 100
# max_depth = 3
# trees = train_random_forest(X_train.values, y_train.values, n_trees=n_trees, max_depth=max_depth)

# # Dự đoán và đánh giá với MSE
# y_pred = predict_random_forest(trees, X_test.values)
# mse = mean_squared_error(y_test.values, y_pred)
# print(f"MSE của mô hình Random Forest: {mse}")

# # Lưu mô hình vào file PKL
# joblib.dump(trees, 'random_forest_model.pkl')
# print("✅ Đã lưu mô hình vào 'random_forest_model.pkl'")

 
import joblib

# Đọc dữ liệu
X_train = pd.read_csv("dataset/X_train.csv")
X_test = pd.read_csv("dataset/X_test.csv")
y_train = pd.read_csv("dataset/y_move_train.csv")
y_test = pd.read_csv("dataset/y_move_test.csv")


# Tạo mô hình Random Forest hồi quy
model = RandomForestRegressor(n_estimators=100, max_depth=3)

# Huấn luyện mô hình
model.fit(X_train, y_train)

# Dự đoán và đánh giá với MSE
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"MSE của mô hình Random Forest: {mse}")

# Lưu mô hình vào file PKL
joblib.dump(model, 'random_forest_model2.pkl')
print("✅ Đã lưu mô hình vào 'random_forest_model.pkl'")
