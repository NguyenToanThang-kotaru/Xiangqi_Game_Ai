import joblib

# Tải mô hình đã huấn luyện
model = joblib.load('ai/random_forest_move_predictor.pkl')

# Kiểm tra số cột trong mô hình và dữ liệu đầu vào
print(f"Model features: {model.feature_names_in_}")
