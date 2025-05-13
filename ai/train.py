import numpy as np
import pandas as pd
import joblib

# Hàm tính MSE
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Hàm chia dữ liệu theo ngưỡng phân chia
def split_data(X, y, feature_index, threshold):
    left_mask = X[:, feature_index] <= threshold
    right_mask = X[:, feature_index] > threshold
    left_X, right_X = X[left_mask], X[right_mask]
    left_y, right_y = y[left_mask], y[right_mask]
    
    # Kiểm tra nếu nhóm bị trống
    if len(left_y) == 0 or len(right_y) == 0:
        return None, None, None, None
    
    return left_X, right_X, left_y, right_y

# Hàm xây dựng cây quyết định
def build_decision_tree(X, y, max_depth=3, max_features=None, depth=0):
    n_samples, n_features = X.shape
    if depth >= max_depth or n_samples <= 1:
        return np.mean(y)  # Trả về giá trị trung bình của nhãn trong nhóm
    
    best_mse = float('inf')
    best_split = None
    
    # Nếu max_features không phải None, chỉ sử dụng một số đặc trưng ngẫu nhiên
    if max_features is not None:
        feature_indices = np.random.choice(n_features, size=max_features, replace=False)
    else:
        feature_indices = range(n_features)  # Sử dụng tất cả đặc trưng
    
    # Duyệt qua tất cả các đặc trưng (hoặc chỉ một phần của chúng)
    for feature_index in feature_indices:
        thresholds = np.unique(X[:, feature_index])  # Các ngưỡng có thể
        for threshold in thresholds:
            # Chia dữ liệu theo ngưỡng
            left_X, right_X, left_y, right_y = split_data(X, y, feature_index, threshold)
            if left_X is None:  # Nếu nhóm con rỗng, bỏ qua
                continue
            # Tính MSE cho phân chia này
            mse = (mean_squared_error(left_y, np.mean(left_y)) * len(left_y) +
                   mean_squared_error(right_y, np.mean(right_y)) * len(right_y)) / len(y)
            if mse < best_mse:
                best_mse = mse
                best_split = (feature_index, threshold)
                best_left_y = left_y
                best_right_y = right_y
    
    # Phân chia dữ liệu và xây dựng các nhánh con
    if best_split is None:
        return np.mean(y)  # Không tìm thấy ngưỡng, trả về trung bình

    left_X, right_X, left_y, right_y = split_data(X, y, best_split[0], best_split[1])

    left_node = build_decision_tree(left_X, left_y, max_depth, max_features, depth + 1)
    right_node = build_decision_tree(right_X, right_y, max_depth, max_features, depth + 1)

    return {"split_feature": best_split[0], "threshold": best_split[1], 
            "left": left_node, "right": right_node}

# Hàm dự đoán với cây quyết định
def predict_decision_tree(tree, X):
    if not isinstance(tree, dict):
        return tree  # Trả về giá trị dự đoán nếu đã tới lá
    if X[tree["split_feature"]] <= tree["threshold"]:
        return predict_decision_tree(tree["left"], X)
    else:
        return predict_decision_tree(tree["right"], X)

# Huấn luyện Random Forest
def train_random_forest(X, y, n_trees=100, max_depth=3, max_features=None):
    trees = []
    n_samples = len(X)
    for _ in range(n_trees):
        # Sử dụng bootstrap sampling (mẫu ngẫu nhiên có lặp lại)
        sample_indices = np.random.choice(n_samples, size=n_samples, replace=True)
        X_sample = X[sample_indices]
        y_sample = y[sample_indices]
        tree = build_decision_tree(X_sample, y_sample, max_depth, max_features)
        trees.append(tree)
    return trees

# Dự đoán với Random Forest
def predict_random_forest(trees, X):
    # Mỗi cây trả về một giá trị scalar cho mỗi mẫu
    predictions = np.array([predict_decision_tree(tree, x) for tree in trees for x in X])
    # Trả về trung bình cộng của tất cả các dự đoán từ các cây
    return np.mean(predictions.reshape(len(trees), len(X)), axis=0)

# Tiền xử lý dữ liệu và chia dữ liệu train/test (nếu chưa chia)
X_train = pd.read_csv("dataset/X_train.csv")  # 95 cột đặc trưng
X_test = pd.read_csv("dataset/X_test.csv")

y_train = pd.read_csv("dataset/y_move_train.csv")  # 1 cột: winrate
y_test = pd.read_csv("dataset/y_move_test.csv")

# Huấn luyện mô hình Random Forest
n_trees = 500
max_depth = 3
max_features = 15  # Giới hạn số lượng đặc trưng mỗi cây sử dụng

trees = train_random_forest(X_train.values, y_train.values, n_trees=n_trees, max_depth=max_depth, max_features=max_features)

# Dự đoán và đánh giá với MSE
# y_pred = predict_random_forest(trees, X_test.values)
# mse = mean_squared_error(y_test.values, y_pred)
# print(f"MSE của mô hình Random Forest: {mse}")

# Lưu mô hình vào file PKL
joblib.dump(trees, 'random_forest_model.pkl')
print("✅ Đã lưu mô hình vào 'random_forest_model.pkl'")
def fen_to_array(self,fen):
    PIECE_MAPPING = {
        'r': 1, 'n': 2, 'b': 3, 'a': 4, 'k': 5, 'c': 6, 'p': 7,  
        'R': 8, 'N': 9, 'B': 10, 'A': 11, 'K': 12, 'C': 13, 'P': 14,  
    }
    parts = fen.split()
    board_fen = parts[0]  # Phần bàn cờ
    turn = parts[1]  # Lượt đi
    board_array = []
    
    for char in board_fen:
        if char in PIECE_MAPPING:  # Nếu là quân cờ
            board_array.append(PIECE_MAPPING[char])
        elif char.isdigit():  # Nếu là số (ô trống)
            board_array.extend([0] * int(char))  # Thêm đúng số lượng số 0
        elif char == '/':  # Dấu `/` không cần lưu
            continue  
    # Thêm lượt đi vào mảng số (0 nếu là 'w', 1 nếu là 'b')
    turn_value = 0 if turn == 'w' else 1
    return board_array ,turn_value
