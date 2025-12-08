# Petri Net Analysis & Optimization

## Dự án này cung cấp các công cụ để:
- Phân tích **tập trạng thái reachable** của Petri Net bằng BDD.
- Kiểm tra **deadlock**.
- Thực hiện **tối ưu hóa tuyến tính** trên marking (tối đa hóa \(c \cdot M\)).

## Các chức năng chính
- Task 1: Đọc và parse file PNML
- Task 2: Tính toán không gian trạng thái tường minh (Explicit Reachability) dùng BFS và DFS.
- Task 3: Tính toán không gian trạng thái ký hiệu (Symbolic Reachability) dùng Binary Decision Diagrams (BDD).
- Task 4: Phát hiện Deadlock kết hợp ILP + BDD (theo yêu cầu đề bài).
- Task 5: Tối ưu hóa hàm mục tiêu
- Task 6: Xuất hình ảnh Petri Net ra màn hình
---
## Yêu cầu phiên bản
- Python 3.12.3
- numpy 2.3.5
- pytest 9.0.2
- pyeda 0.28.0
- pm4py 2.7.19.3
- WSL (trên Windows) hoặc Linux / macOS
---
# Hướng dẫn chạy code

- 1. Tạo môi trường ảo (virtual environment)
```sh
python3 -m venv venv
```

- 2. Kích hoạt môi trường ảo
```sh
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```
- 3. Cài các thư viện cần thiết (Nếu bạn đã cài ở lần trước thì bỏ qua bước này)

- Cài đặt các thư viện từ `requirements.txt`
```sh
pip install -r requirements.txt
```
- 4. Run code

```sh
python3 run.py
```

- 5. Nhâp tên file

- Nhập file theo cú pháp 

```sh
test_PNML\file_name
```
- Các file có sẵn: 
- Input.pnml
- philo.pnml
- FileAccess.pnml
- ShareMemory_v2.pnml
- ShareMemory.pnml
- SwimmingPool.pnml
- TokenRing.pnml

---

## Cấu trúc dự án

```bash
.
├── src/
│   ├── BDD.py
│   ├── BFS.py
│   ├── Deadlock.py
│   ├── DFS.py
│   ├── Optimization.py  
│   └── PetriNet.py
├── test_PNML/
│   ├── FileAccess.pnml
│   ├── philo.pnml
│   ├── ShareMemory_v2.pnml
│   ├── ShareMemory.pnml
│   ├── SwimmingPool.pnml
│   └── TokenRing.pnml
├── run.py
├── requirements.txt
└── README.md

---
# HO CHI MINH CITY UNIVERSITY OF TECHNOLOGY
# Faculty of Computer Science and Engineering
#Mathematical Modeling - CO2011
