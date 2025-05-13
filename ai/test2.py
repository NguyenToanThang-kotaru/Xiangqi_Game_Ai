import joblib

# Tải mô hình từ tệp .pkl
model = joblib.load('ai/random_forest_model.pkl')

# In thông tin từng cây trong rừn
def predict_decision_tree(tree, X):
    """
    Hàm dự đoán cho một cây quyết định.
    :param tree: Cây quyết định.
    :param X: Dữ liệu đầu vào (vector đặc trưng).
    :return: Dự đoán từ cây quyết định.
    """
    if not isinstance(tree, dict):  # Đến lá của cây, trả về giá trị
        return tree
    
    feature_index = tree['split_feature']
    threshold = tree['threshold']

    if X[feature_index] <= threshold:
        return predict_decision_tree(tree['left'], X)
    else:
        return predict_decision_tree(tree['right'], X)

import numpy as np

def predict_random_forest(trees, X):
    """
    Hàm dự đoán cho Random Forest.
    :param trees: Danh sách các cây quyết định trong Random Forest.
    :param X: Dữ liệu đầu vào (vector đặc trưng).
    :return: Dự đoán trung bình của tất cả các cây.
    """
    predictions = np.array([predict_decision_tree(tree, X) for tree in trees])
    return np.mean(predictions)

# Giả sử bạn có dữ liệu đầu vào (ví dụ: X_test)
X_test = np.array([1,2,3,4,5,0,3,2,1,0,0,0,0,4,0,0,0,0,0,6,0,0,0,0,0,6,0,7,0,7,0,7,0,7,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0,14,0,14,0,14,0,14,0,14,0,0,0,0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,8,9,10,11,12,11,10,9,8,1,1,2,0,2])  # Một ví dụ về dữ liệu đầu vào

# Dự đoán bằng Random Forest
predicted_value = predict_random_forest(model, X_test)

print(f"Dự đoán cho mẫu X_test: {predicted_value}")
