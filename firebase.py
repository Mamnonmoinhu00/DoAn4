import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# Để sử dụng được trên raspberry pi 4 thì phải cài môi trường ảo
# python -m venv myenv --system-site-packages : Tạo mt ảo
# source myenv/bin/activate : Kích hoạt mt ảo
# pip install firebase-admin : Cài firebase-admin
# deactivate : Hủy kích hoạt mt ảo sau khi dùng

# Khởi tạo Firebase Admin SDK
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://traffic-b5082-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def add_location(location_name, congestion, lat, lng):
    # Tạo dữ liệu cho location
    data = {
        'congestion': congestion,
        'lat': lat,
        'lng': lng
    }
    
    # Thêm dữ liệu vào collection 'traffic_data'
    ref = db.reference(f'traffic/{location_name}')
    ref.set(data)  # Sử dụng set() để ghi đè dữ liệu nếu đã tồn tại
    print(f'Location {location_name} added with data: {data}')

# # Dữ liệu cho một location mới
# location_name = 'location4'  # Tên của location
# congestion = 1  # Mức độ ùn tắc
# lat = 21.031  # Vĩ độ
# lng = 105.851  # Kinh độ

# # Gọi hàm để thêm location
# add_location(location_name, congestion, lat, lng)
