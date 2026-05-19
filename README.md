# Gomoku AI - Minimax & Alpha-Beta

## Giới thiệu

Đây là chương trình game Caro (Gomoku) được xây dựng bằng Python và Tkinter.

Chương trình sử dụng:
- Thuật toán Minimax
- Thuật toán Alpha-Beta Pruning
- Chế độ Compare để so sánh hiệu năng của hai thuật toán

Người chơi sẽ đánh với AI trên bàn cờ 9x9 và cần tạo được 4 quân liên tiếp để chiến thắng.

---

# Cấu trúc thư mục

```bash
source_code/
│
├── ai.py
├── board.py
├── main.py
│
├── README.md
├── requirements.txt
└── report.pdf
```

---

# Chức năng chính

- Chơi Caro với AI
- Chọn thuật toán:
  - Minimax
  - Alpha-Beta
  - Compare Mode
- Chọn độ sâu tìm kiếm
- Chọn người đi trước
- Hiển thị:
  - Thời gian suy nghĩ
  - Số node đã duyệt
  - Tốc độ xử lý
  - Nước đi AI chọn

---

# Cách cài đặt

## 1. Cài Python

Yêu cầu:
- Python 3.10 trở lên

Kiểm tra:

```bash
python --version
```

---

## 2. Cài thư viện

Mở terminal trong thư mục project:

```bash
pip install -r requirements.txt
```

---

# Cách chạy chương trình

Di chuyển vào thư mục source_code:

```bash
cd source_code
```

Chạy file main:

```bash
python main.py
```

---

# Hướng dẫn sử dụng

## Bước 1
Chọn:
- Thuật toán
- Độ sâu tìm kiếm
- Người đi trước

## Bước 2
Nhấn nút **BẮT ĐẦU**

## Bước 3
Click chuột lên bàn cờ để đánh.

---

# Compare Mode

Ở chế độ Compare:
- AI sẽ chạy cả Minimax và Alpha-Beta
- Hiển thị:
  - Thời gian chạy
  - Số node đã duyệt
  - Tốc độ xử lý
  - Nước đi mà mỗi thuật toán chọn
