cat > README.md << 'EOF'
# Petri Net Analysis & Optimization

Dự án này cung cấp các công cụ để:
- Phân tích **tập trạng thái reachable** của Petri Net bằng BDD.
- Kiểm tra **deadlock**.
- Thực hiện **tối ưu hóa tuyến tính** trên marking (tối đa hóa \(c \cdot M\)).

---

## 1. Yêu cầu môi trường

- Python 3.x
- \`git\` (nếu bạn clone project từ repository)
- VS Code (khuyến khích)
- WSL (trên Windows) hoặc Linux / macOS

---

## 2. Thiết lập và kích hoạt môi trường ảo

- Tạo môi trường ảo (virtual environment)
```sh
python3 -m venv venv
```

- Kích hoạt môi trường ảo
```sh
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```
## 3. Cài cái thư viện cần thiết

- Cài đặt các thư viện từ `requirements.txt`
```sh
pip install -r requirements.txt
```

## 4. Yêu cầu file pnml input

- Mặc định trong chương trình sử dụng file
```sh
Input_pnml_file.pnml
```
- Nếu muốn test với file pnml khác bạn làm như sau
- 1. Chuẩn bị file `.pnml` mới, đảm bảo đúng định dạng PNML mà chương trình hỗ trợ.
- 2. Copy file mới và dán đè lên `example.pnml` (hoặc sửa lại code để trỏ đến tên file bạn muốn).
- 3. Mở file `run.py`, kéo xuống phần:
``` sh
# 6. Optimization: maximize c·M
c = [...]
```
- 4. Cập nhật mảng c sao cho số phần tử mảng c bằng số phần tử place

## 5. Chạy chương trình 

- Sau khi thực hiện các mục 1 2 3 4, vào terminal và nhập lênh:
```sh
python3 run.py
```