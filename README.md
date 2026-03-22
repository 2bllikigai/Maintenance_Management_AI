# 🛠️ Hệ thống Quản lý & Dự báo Bảo trì Tài sản (Odoo AI)

Dự án được phát triển bởi **Kiều Quang Trường** - Sinh viên chuyên ngành Công nghệ thông tin, trường **Đại học Đại Nam**. Hệ thống được xây dựng trên nền tảng Odoo, tích hợp mô hình Machine Learning để tối ưu hóa công tác bảo trì tài sản trong doanh nghiệp.

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Odoo](https://img.shields.io/badge/Odoo-16.0+-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)

---

## 🌟 1. Tổng quan dự án

Hệ thống tập trung vào việc số hóa quy trình quản lý tài sản và sử dụng dữ liệu lịch sử để đưa ra các dự báo thông minh, giúp giảm thiểu rủi ro hỏng hóc bất ngờ.

### Các tính năng chính:
* **Quản lý tài sản (Assets):** Theo dõi chi tiết danh mục thiết bị, giá trị khấu hao và trạng thái vận hành.
* **Lịch sử bảo trì (Maintenance History):** Ghi chép toàn bộ quá trình sửa chữa, chi phí phát sinh và tình trạng thiết bị sau bảo trì.
* **Dự báo AI (AI Prediction):** * Sử dụng thuật toán **Linear Regression** (Hồi quy tuyến tính) để phân tích chu kỳ bảo trì.
    * Tự động tính toán và hiển thị **Ngày bảo trì dự kiến (AI)**.
* **Quản trị dữ liệu:** Hỗ trợ công cụ Import/Export linh hoạt từ Excel.

---

## 🚀 2. Cài đặt & Triển khai

### 2.1. Cài đặt môi trường
Người sử dụng thực thi lệnh sau để cài đặt các thư viện hệ thống cần thiết:
```bash
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-dev libpq-dev
```
### 2.2. Khởi tạo dự án 
#### 1.Clone project :
```bash
git clone [https://github.com/2bllikigai/Maintenance_Management_AI.git](https://github.com/2bllikigai/Maintenance_Management_AI.git)
cd Maintenance_Management_AI
```
#### 2.Thiết lập môi trường ảo (Virtual Environment):
```bash
python3.10 -m venv venv
source venv/bin/activate  # Đối với Linux/Ubuntu
# Hoặc .\venv\Scripts\activate nếu sử dụng Windows
```
#### 3. Cài đặt các thư viện Python cần thiết :
```bash
pip install -r requirements.txt
```
### 2.3. Cấu hình hệ thống Odoo
Tạo tệp odoo.conf (có thể kế thừa từ odoo.conf.template) với nội dung sau:
```toml
[options]
addons_path = addons
db_host = localhost
db_user = odoo
db_password = odoo
db_port = 5432
xmlrpc_port = 8069
```
## 📊3. Hướng dẫn sử dụng tính năng AI & Import
### 3.1. Nạp dữ liệu lịch sử bảo trì (Data Preparation)

Để mô hình Machine Learning hoạt động chính xác, dữ liệu đầu vào đóng vai trò quan trọng:

1. Truy cập vào module **Assets (Tài sản)** → Menu **Lịch sử bảo trì**.
2. Chọn **Favorites → Import records** và tải lên file dữ liệu Excel.
3. **Lưu ý kỹ thuật:**  
   Tại màn hình cấu hình các trường dữ liệu, bạn phải **BỎ TÍCH ô `Allow matching with subfields`** ở thanh công cụ bên trái.  
   Điều này giúp hệ thống nhận diện đúng các trường dữ liệu chính như **Maintenance Date** và **Asset** mà không bị nhầm lẫn với các thuộc tính con khác.

### 3.2. Vận hành dự báo AI

Sau khi dữ liệu lịch sử được nạp thành công:

- Thuật toán **Linear Regression** sẽ tự động phân tích tần suất và chu kỳ bảo trì của từng loại tài sản.
- Hệ thống sẽ tự động cập nhật và hiển thị **Ngày bảo trì dự kiến (AI)** ngay trên giao diện danh sách tài sản.
- Người quản lý có thể dựa vào thông tin này để lên kế hoạch bảo trì chủ động.
## 📂 4. Cấu trúc Module
```plaintext
MaintenanceManagement_AI/
├── __manifest__.py  # Tệp khai báo thông tin module của cả dự án
├── __init__.py         # Tệp import từng module
├── models/             # Định nghĩa logic nghiệp vụ và cấu trúc Database
├── views/              # Giao diện người dùng (List view, Form view)
├── AI_Management/      # Thư mục chứa code xử lý thuật toán AI (Python)
├── security/           # Định nghĩa quyền truy cập
├── data/               # Chứa các tệp dữ liệu mẫu
└── __manifest__.py     # Tệp khai báo thông tin module
```
## 👨‍💻 5. Thông tin tác giả
**Thực hiện bởi:** Nhóm 5

**Thành viên:** Kiều Quang Trường (08/11/2005) cùng các thành viên Nhóm 5.

**Đề tài:** Ứng dụng **Machine Learning** vào quản trị hệ thống bảo trì trên nền tảng **Odoo**.