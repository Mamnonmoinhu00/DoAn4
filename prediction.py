import pandas as pd
import joblib

# Tải mô hình đã lưu
model = joblib.load('logistic_regression_model.pkl')

def predict_traffic_condition(longitude, latitude, hour, flow):
    # Bước 1: Chuyển đổi dữ liệu đầu vào thành DataFrame
    input_data = pd.DataFrame({
        'Long': [longitude],
        'Lat': [latitude],
        'Time': [hour],
        'Flow': [flow]
    })

    # Bước 2: Dự đoán tình trạng giao thông
    prediction = model.predict(input_data)
    # Bước 3: Trả về kết quả
    return 1 if prediction[0] == 1 else 0

# Ví dụ sử dụng hàm
# hour_input = int(input("Nhập thời gian: "))
# flow_input = int(input("Nhập lưu lượng xe: "))

# result = predict_traffic_condition(105.849, 21.0285, hour_input, flow_input)
# print(f'{hour_input},{flow_input}: Dự đoán tình trạng giao thông: {result}')