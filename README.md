# 📄 Hướng Dẫn Cấu Hình Wkhtmltopdf Trong Odoo (Windows)

## 🧩 1. Giới Thiệu

**Wkhtmltopdf** là công cụ giúp **Odoo** chuyển đổi nội dung HTML sang định dạng **PDF** — ví dụ như in báo cáo, hóa đơn, hợp đồng, v.v.  
Để Odoo sử dụng được Wkhtmltopdf, cần cấu hình **đường dẫn thực thi** (executable path) trong hệ thống.

---

## ⚙️ 2. Thêm Wkhtmltopdf Vào Cấu Hình Odoo

### **Bước 1:** Bật chế độ Developer mode  
- Trong Odoo, truy cập:
  ```
  Settings → Developer Mode → Activate the Developer Mode
  ```
  (Hoặc thêm `?debug=1` vào cuối URL trình duyệt.)

### **Bước 2:** Thêm System Parameter  
- Truy cập:  
  ```
  Settings → Technical → System Parameters
  ```
- Nhấn **“New”** và nhập:

  | Key | Value |
  |-----|--------|
  | `wkhtmltopdf` | `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf` |

- Lưu lại thay đổi.

---

## 🧠 3. Cấu Hình Biến Môi Trường Trên Windows

### **Bước 1:** Mở cửa sổ **Edit System Environment Variables**
- Nhấn **Windows + S** → gõ `environment variables` → chọn **Edit the system environment variables**.

### **Bước 2:** Cập nhật biến PATH

Thêm đường dẫn sau vào cả **User variables** và **System variables**:
```
C:\Program Files\wkhtmltopdf\bin
```

> ⚠️ **Lưu ý:**  
> - Nếu đã có PATH cũ, chỉ cần **thêm mới dòng này**, không xóa các giá trị khác.  
> - Đảm bảo đường dẫn chính xác với nơi cài đặt wkhtmltopdf trên máy bạn.

---

## 🔄 4. Khởi Động Lại Máy

Sau khi hoàn tất, **restart máy tính** để các biến môi trường có hiệu lực.

---

## ✅ 5. Kiểm Tra

Để kiểm tra cấu hình:
1. Mở **Command Prompt (CMD)**  
2. Gõ lệnh:
   ```bash
   wkhtmltopdf --version
   ```
3. Nếu thấy hiện phiên bản như:
   ```
   wkhtmltopdf 0.12.6 (with patched qt)
   ```
   → nghĩa là đã cài đặt và cấu hình thành công.

---

## 📘 6. Tóm Tắt Nhanh

- [x] Bật Developer mode  
- [x] Thêm **System Parameter** trong Odoo  
- [x] Cập nhật **PATH** trong Windows  
- [x] **Restart máy**  
- [x] Kiểm tra bằng lệnh `wkhtmltopdf --version`
