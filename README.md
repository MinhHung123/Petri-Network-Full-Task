## Cách setup để chạy code
- Mở project bằng wsl trên vscode (giống như làm lab bên môn hệ điều hành)

- Mở new terminal và vào đúng thư mục TASK6_BTL_HK251-MAIN

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

- Cài đặt các thư viện từ `requirements.txt`
```sh
pip install -r requirements.txt
```
- T để cái file pnml input mặc định trong example.pnml nhe. Nếu ae muốn test file pnml khác thì:
- B1: Copy file pnml mới và dán đè vào file pnml cũ (file mới phải đảm bảo đúng định dạng nhe ko thì nó đọc ko đc)
- B2: vào file run.py vào kéo xuống dưới tới chỗ 6. Optimization: maximize c·M và đổi mảng c sao cho phần tử mảng c bằng số place của file mới của ae

## Running Code
```sh
python3 run.py
```


