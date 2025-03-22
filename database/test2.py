import pandas as pd

df = pd.read_csv("processed_data.csv")


print(df.head())  # Hiển thị 5 dòng đầu tiên
print(df.info())  # Kiểm tra thông tin cột
