# BÁO CÁO TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM
## ĐỀ TÀI 03: WEBSITE QUẢNG BÁ SẢN PHẨM (WORDPRESS)

* **Sinh viên thực hiện:** Mai Đăng Cường
* **Mã số sinh viên:** DTC245200425
* **Repository GitHub:** [https://github.com/maidangcuong/DTC245200425](https://github.com/maidangcuong/DTC245200425)

---

## 1. Tổng quan kiến trúc hệ thống (Architecture)

Hệ thống được đóng gói hoàn toàn bằng **Docker Compose**, bao gồm các thành phần chính:
1. **Web Application & Database:**
   - **WordPress (`wordpress:latest`)**: Nền tảng CMS quảng bá sản phẩm.
   - **MySQL 8.0 (`mysql:8.0`)**: Cơ sở dữ liệu quan hệ lưu trữ dữ liệu WordPress.
   - **phpMyAdmin (`phpmyadmin/phpmyadmin`)**: Giao diện trực quan quản lý CSDL MySQL.
2. **Reverse Proxy & Security:**
   - **Nginx (`nginx:alpine`)**: Reverse proxy điều phối luồng mạng, cấu hình SSL/TLS (HTTPS tự ký), chuyển hướng tự động HTTP (80) -> HTTPS (443), tích hợp đầy đủ HTTP Security Headers.
3. **Giám sát hệ thống (Monitoring & Visualization):**
   - **cAdvisor (`gcr.io/cadvisor/cadvisor`)**: Thu thập metrics tài nguyên container (CPU, RAM, Network, I/O).
   - **mysqld-exporter (`prom/mysqld-exporter`)**: Thu thập metrics chuyên sâu của MySQL.
   - **nginx-prometheus-exporter (`nginx/nginx-prometheus-exporter`)**: Thu thập metrics truy cập của web server Nginx qua stub_status.
   - **Prometheus (`prom/prometheus:latest`)**: Time-series database thu thập và lưu trữ toàn bộ metrics từ các exporters.
   - **Grafana (`grafana/grafana:latest`)**: Dashboard trực quan hóa toàn bộ metrics giám sát.
4. **Log tập trung (Centralized Logging):**
   - **Promtail (`grafana/promtail:latest`)**: Agent thu thập log Nginx (Access log & Error log).
   - **Loki (`grafana/loki:latest`)**: Hệ thống lưu trữ và đánh chỉ mục log tập trung.
5. **Bảo mật & Hardening:**
   - **Network Isolation:** Phân tách rõ ràng mạng `frontend-net` (Web/Proxy/Monitoring) và `backend-net` (Database/Exporters). Database MySQL không bị public port ra môi trường bên ngoài.
   - **Bảo vệ thông tin bí mật:** Sử dụng `.env` để quản lý mật khẩu và cấu hình nhạy cảm.

---

## 2. Danh mục dịch vụ & Cổng truy cập (Service Endpoints)

| Dịch vụ | Địa chỉ truy cập / Port | Chức năng chính |
| :--- | :--- | :--- |
| **WordPress (Website)** | `https://localhost` | Website quảng bá sản phẩm chính thức |
| **phpMyAdmin** | `https://localhost/phpmyadmin/` | Quản trị Database MySQL qua giao diện web |
| **Nginx (HTTP -> HTTPS)** | `http://localhost:80` | Tự động chuyển hướng sang HTTPS (Port 443) |
| **Grafana Dashboard** | `http://localhost:3001` | Theo dõi hiệu năng hệ thống, metrics và log |
| **Prometheus Web UI** | `http://localhost:9090` | Xem trạng thái scrape targets và truy vấn PromQL |
| **Loki API** | `http://localhost:3100` | Endpoint tiếp nhận và xử lý LogQL |

---

## 3. Hướng dẫn khởi chạy hệ thống (Quick Start)

### Bước 1: Chuẩn bị môi trường & Biến môi trường
Sao chép file `.env.example` thành `.env` (nếu chưa có):
```bash
cp .env.example .env
```

### Bước 2: Khởi chạy toàn bộ hệ thống
Sử dụng Docker Compose để build và chạy toàn bộ containers:
```bash
docker compose up -d
```

### Bước 3: Kiểm tra trạng thái containers
```bash
docker compose ps
```

---

## 4. Mẫu truy vấn LogQL trên Grafana (Loki)

Truy cập Grafana tại `http://localhost:3001` -> Menu **Explore** -> Chọn Data Source **Loki**:

1. **Xem toàn bộ log truy cập của Nginx:**
   ```logql
   {job="nginx"}
   ```
2. **Lọc các request HTTP gặp lỗi (4xx và 5xx):**
   ```logql
   {job="nginx"} |~ " (4[0-9]{2}|5[0-9]{2}) "
   ```
3. **Thống kê tần suất request theo thời gian:**
   ```logql
   rate({job="nginx"}[1m])
   ```

---

## 5. Lịch sử các bước triển khai (Commit History)
* **Commit 1:** `Add Nginx reverse proxy with HTTPS self-signed and security headers`
* **Commit 2:** `Setup Prometheus, Exporters, and Grafana for monitoring`
* **Commit 3:** `Add Loki, Promtail centralized logging and system hardening`
* **Commit 4:** `Optimize configuration, add network isolation, exporters, and documentation`
