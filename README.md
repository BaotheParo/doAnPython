# Game Farm Fishing

## Mô tả dự án
Game Farm Fishing là một trò chơi mô phỏng nông trại và câu cá, nơi người chơi có thể trồng cây, câu cá và quản lý tài sản của mình.
Có thể đọc mô tả game ở đây 
### https://docs.google.com/document/d/1YOmYwj3osB3sTet5VCWltF7gZDhyAV7FLrGlSqtGQww/edit?usp=sharing

## Cấu trúc thư mục
```
Game_Farm_Fishing/
├── main.py 				# File chính để chạy game
├── src/ 				# Thư mục chứa mã nguồn
│ ├── core/ 				# Các module cơ bản, dùng chung
│ │ ├── player.py 			# Quản lý thuộc tính người chơi (năng lượng, kho đồ, tiền)
│ │ ├── time_system.py 			# Hệ thống thời gian (ngày/đêm)
│ │ ├── inventory.py 			# Quản lý kho đồ
│ │ └── ui.py 				# Giao diện chung (icon, đồng hồ, bánh răng)
│ ├── scenes/ 				# Các màn hình trong game
│ │ ├── menu.py 			# Menu chính (Bắt đầu, Tiếp tục, Thoát)
│ │ ├── bedroom.py 			# Phòng ngủ (giường, cửa)
│ │ ├── farm.py 			# Nông trại (khu vườn, cửa, biển hiệu)
│ │ ├── village.py 			# Làng (thương nhân, biển hiệu)
│ │ └── fishing.py 			# Câu cá (ao, biển hiệu)
│ ├── actions/ 				# Các hành động cụ thể
│ │ ├── planting.py 			# Trồng cây (gieo hạt, tưới, thu hoạch, đào)
│ │ └── fishing_action.py 		# Hành động câu cá
│ └── utils/ 				# Các công cụ hỗ trợ
│ ├── save_load.py 			# Lưu và tải game
│ └── constants.py 			# Hằng số (giá tiền, năng lượng, thời gian trồng cây)
├── assets/ 				# Tài nguyên tĩnh
│ ├── images/ 				# Hình ảnh
│ │ ├── icons/ 				# Đồng hồ, bánh răng
│ │ ├── plants/ 			# Hình ảnh cây (cà rốt, bắp cải, v.v.)
│ │ ├── fish/ 				# Hình ảnh cá
│ │ └── backgrounds/ 			# Hình nền (phòng ngủ, nông trại, làng, ao)
│ ├── sounds/ 				# Âm thanh (nếu có)
│ └── fonts/ 				# Font chữ
├── saves/ 				# Thư mục lưu file save game
│ ├── save1.dat 			# File save của người chơi 1
│ ├── save2.dat 			# File save của người chơi 2
│ └── ...
├── readme.md 				# Tài liệu
└── requirements.txt 			# Danh sách thư viện cần cài (nếu dùng Pygame, v.v.)
```