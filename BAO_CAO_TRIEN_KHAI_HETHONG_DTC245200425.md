# BÁO CÁO TỔNG HỢP BÀI TẬP LỚN
# MÔN: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

---

### **ĐỀ TÀI SỐ 03: XÂY DỰNG VÀ QUẢN TRỊ HỆ THỐNG WEBSITE QUẢNG BÁ SẢN PHẨM (WORDPRESS) TRÊN NỀN TẢNG DOCKER COMPOSE, NGINX REVERSE PROXY, PROMETHEUS, GRAFANA VÀ LOKI**

---

* **Sinh viên thực hiện:** Mai Đăng Cường
* **Mã số sinh viên:** DTC245200425
* **Lớp:** Triển khai và Quản trị Hệ thống Phần mềm
* **Repository GitHub:** [https://github.com/maidangcuong/DTC245200425](https://github.com/maidangcuong/DTC245200425)
* **Năm học:** 2026 - 2027

---

\newpage

## MỤC LỤC

1. **CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI VÀ MỤC TIÊU TRIỂN KHAI**
   * 1.1. Bối cảnh và Đặt vấn đề
   * 1.2. Mục tiêu của đề tài
   * 1.3. Yêu cầu kỹ thuật theo đề bài
2. **CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG TỔNG THỂ**
   * 2.1. Sơ đồ kiến trúc phân tầng (Architecture Diagram)
   * 2.2. Danh mục các dịch vụ và Container trong hệ thống
   * 2.3. Thiết kế luồng mạng và Phân vùng mạng (Network Isolation)
3. **CHƯƠNG 3: TRIỂN KHAI ỨNG DỤNG WEB, CSDL VÀ NGINX REVERSE PROXY (COMMIT 1)**
   * 3.1. Cấu hình CSDL MySQL 8.0 và phpMyAdmin
   * 3.2. Cấu hình Web Application WordPress (Showroom TechStore)
   * 3.3. Cấu hình Nginx Reverse Proxy và Chứng chỉ số SSL/TLS tự ký
   * 3.4. Minh chứng kết quả triển khai Chương 3
4. **CHƯƠNG 4: HỆ THỐNG GIÁM SÁT HIỆU NĂNG PROMETHEUS VÀ GRAFANA (COMMIT 2)**
   * 4.1. Nguyên lý hoạt động của Prometheus và các Exporter
   * 4.2. Cấu hình cAdvisor (Giám sát tài nguyên Container)
   * 4.3. Cấu hình mysqld-exporter (Giám sát Cơ sở dữ liệu)
   * 4.4. Cấu hình nginx-prometheus-exporter (Giám sát Web Server)
   * 4.5. Xây dựng Dashboard trực quan hóa trên Grafana
   * 4.6. Minh chứng kết quả triển khai Chương 4
5. **CHƯƠNG 5: HỆ THỐNG QUẢN LÝ NHẬT KÝ TẬP TRUNG LOKI VÀ PROMTAIL (COMMIT 3)**
   * 5.1. Kiến trúc thu thập log với Promtail và lưu trữ trên Loki
   * 5.2. Cấu hình pipeline đọc log Nginx
   * 5.3. Xây dựng và thực thi các câu truy vấn LogQL thực tế
   * 5.4. Minh chứng kết quả triển khai Chương 5
6. **CHƯƠNG 6: CÁC GIẢI PHÁP BẢO MẬT (HARDENING) VÀ QUẢN LÝ MÃ NGUỒN GITHUB**
   * 6.1. Phân tích các giải pháp Hardening đã áp dụng
   * 6.2. Quản lý cấu hình bí mật qua Biến môi trường (.env)
   * 6.3. Quản lý mã nguồn theo chuẩn Git Workflow trên GitHub
   * 6.4. Minh chứng kết quả triển khai Chương 6
7. **CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**
   * 7.1. Đánh giá kết quả đạt được
   * 7.2. Bài học kinh nghiệm
   * 7.3. Hướng phát triển trong tương lai
8. **TÀI LIỆU THAM KHẢO**

---

\newpage

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI VÀ MỤC TIÊU TRIỂN KHAI

### 1.1. Bối cảnh và Đặt vấn đề
Trong kỷ nguyên số hóa và điện toán đám mây, việc triển khai một ứng dụng phần mềm không đơn thuần là cài đặt mã nguồn lên một máy chủ vật lý, mà đòi hỏi quy trình tự động hóa, tính mở rộng cao, đảm bảo an toàn thông tin và khả năng quan sát toàn diện (Observability). 

Đề tài số 03 tập trung vào bài toán thực tế: **"Triển khai và Quản trị Hệ thống Website Quảng bá Sản phẩm sử dụng WordPress"**. Thay vì cài đặt truyền thống, hệ thống được thiết kế theo tiêu chuẩn DevOps hiện đại, ứng dụng công nghệ container hóa với Docker Compose, định tuyến bảo mật qua Nginx Reverse Proxy HTTPS, kết hợp bộ giải pháp giám sát metrics (Prometheus + Grafana) và quản lý log tập trung (Loki + Promtail).

### 1.2. Mục tiêu của đề tài
* **Về mặt Triển khai (Deployment):** Đóng gói toàn bộ các dịch vụ (Web, DB, Tool, Proxy, Exporters, Monitoring, Logging) thành một tệp điều phối `docker-compose.yml` duy nhất, cho phép khởi chạy toàn bộ hệ thống bằng một câu lệnh duy nhất (`docker compose up -d`).
* **Về mặt Bảo mật (Security & Hardening):** Áp dụng mô hình Reverse Proxy với HTTPS tự ký (Self-signed Certificate), cấu hình các HTTP Security Headers chuẩn OWASP, phân tách mạng nội bộ (Network Isolation) để cô lập cơ sở dữ liệu.
* **Về mặt Quản trị (Administration & Monitoring):** Giám sát thời gian thực trạng thái CPU, RAM của từng container, tần suất truy vấn CSDL MySQL và lưu lượng request của Nginx Web Server.
* **Về mặt Giám sát Nhật ký (Logging):** Thu thập toàn bộ nhật ký truy cập (Access log) và nhật ký lỗi (Error log) của máy chủ Nginx về hệ thống Loki, phân tích và lọc sự cố bằng ngôn ngữ LogQL.

### 1.3. Bảng tổng hợp Yêu cầu kỹ thuật và Barem điểm

| STT | Hạng mục đánh giá | Yêu cầu kỹ thuật chi tiết | Điểm |
| :---: | :--- | :--- | :---: |
| 1 | Quản lý mã nguồn GitHub | Repo đặt tên theo MSSV (`DTC245200425`), đủ 3+ commit tiến độ, có README.md chi tiết. | 1.5 |
| 2 | Triển khai App + Database | WordPress chạy ổn định, kết nối MySQL 8.0, phpMyAdmin quản trị DB hoạt động. | 1.5 |
| 3 | Nginx Reverse Proxy | Định tuyến domain, chuyển hướng HTTP 80 -> HTTPS 443, SSL tự ký, Security Headers. | 1.5 |
| 4 | Hệ thống giám sát (Prometheus + Grafana) | Thu thập metrics Container, Web, DB qua Exporters; Dashboard Grafana trực quan. | 1.5 |
| 5 | Hệ thống Log tập trung (Loki + Promtail) | Promtail gom log Nginx về Loki, chạy ít nhất 2–3 câu truy vấn LogQL thực tế. | 1.5 |
| 6 | Hardening hệ thống | Áp dụng 3–4 biện pháp: Network isolation, non-root, mật khẩu mạnh, ẩn port DB. | 1.5 |
| 7 | Báo cáo & Trình bày | Báo cáo $\ge 10$ trang, đầy đủ sơ đồ kiến trúc, giải thích chi tiết, minh chứng rõ ràng. | 1.0 |
| **TỔNG** | **HỆ THỐNG HOÀN CHỈNH** | **ĐẠT CHUẨN TẤT CẢ CÁC TIÊU CHÍ ĐỀ BÀI ĐƯA RA** | **10.0** |

---

\newpage

# CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG TỔNG THỂ

### 2.1. Sơ đồ kiến trúc phân tầng (Architecture Diagram)

Hệ thống được thiết kế theo mô hình Microservices phân tầng chặt chẽ:

```
                                [ CLIENT / TRÌNH DUYỆT ]
                                           │
                        (Port 80: HTTP Redirect & Port 443: HTTPS)
                                           ▼
                 ┌───────────────────────────────────────────────────┐
                 │       NGINX REVERSE PROXY (Port 80, 443)          │
                 │   - SSL/TLS Termination (nginx.crt, nginx.key)    │
                 │   - Security Headers (X-Frame, CSP, XSS, nosniff) │
                 └─────────────┬───────────────────────┬─────────────┘
                               │ (proxy_pass /)        │ (proxy_pass /phpmyadmin/)
                               ▼                       ▼
   ┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
   │    WORDPRESS APPLICATION (Port 80)  │   │       PHPMYADMIN (Port 80)          │
   │  - Theme Astra: Showroom TechStore  │   │  - Giao diện quản trị web cho DB    │
   └──────────────────┬──────────────────┘   └──────────────────┬──────────────────┘
                      │                                         │
                      └────────────────────┬────────────────────┘
                                           │ (Kết nối TCP: Port 3306)
                                           ▼
                 ┌───────────────────────────────────────────────────┐
                 │              MYSQL 8.0 DATABASE SERVER            │
                 │   - CSDL: wordpress_db (Cô lập trong backend-net) │
                 │   - Lưu trữ dữ liệu bền vững qua Named Volume     │
                 └───────────────────────────────────────────────────┘

  ═════════════════════════ HỆ THỐNG GIÁM SÁT & QUẢN TRỊ ═════════════════════════

    [ CẢM BIẾN / EXPORTERS ]            [ THU THẬP & LƯU TRỮ ]         [ TRỰC QUAN HÓA ]
   ┌────────────────────────┐          ┌──────────────────────┐      ┌──────────────────┐
   │ cAdvisor (Container)   │ ──(Pull)─►                      │      │                  │
   ├────────────────────────┤          │ Prometheus Server    │─────►│ Grafana          │
   │ mysqld-exporter (DB)   │ ──(Pull)─► (Port 9090)          │      │ Dashboard        │
   ├────────────────────────┤          └──────────────────────┘      │ (Port 3001)      │
   │ nginx-exporter (Web)   │ ──(Pull)─►                             │                  │
   └────────────────────────┘                                        │ - Xem Metrics    │
                                                                     │ - Xem LogQL      │
   ┌────────────────────────┐          ┌──────────────────────┐      │                  │
   │ Promtail Agent         │ ──(Push)─► Loki Log Server      │─────►│                  │
   │ (Đọc log Nginx /logs)  │          │ (Port 3100)          │      │                  │
   └────────────────────────┘          └──────────────────────┘      └──────────────────┘
```

### 2.2. Danh mục các dịch vụ và Container trong hệ thống

| Tên Service | Tên Container | Image sử dụng | Cổng nội bộ | Cổng Public ra Host | Vai trò chức năng |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`nginx`** | `nginx_proxy` | `nginx:alpine` | 80, 443 | **80, 443** | Cổng vào duy nhất, Reverse Proxy, mã hóa SSL, bảo mật HTTP headers. |
| **`wordpress`** | `wordpress_app` | `wordpress:latest` | 80 | *Không mở* | Ứng dụng web quảng bá sản phẩm công nghệ (TechStore). |
| **`db`** | `wordpress_db` | `mysql:8.0` | 3306 | *Không mở* | CSDL MySQL lưu trữ bài viết, người dùng, sản phẩm. |
| **`phpmyadmin`**| `wordpress_phpmyadmin` | `phpmyadmin/phpmyadmin` | 80 | *Không mở* | Quản trị CSDL qua giao diện web tại `/phpmyadmin/`. |
| **`cadvisor`** | `cadvisor_metrics` | `gcr.io/cadvisor/cadvisor:v0.47.0` | 8080 | *Không mở* | Thu thập thông số phần cứng (CPU, RAM, Network) của các containers. |
| **`mysqld-exporter`** | `mysql_exporter` | `prom/mysqld-exporter:v0.15.1` | 9104 | *Không mở* | Thu thập chỉ số truy vấn, kết nối, bộ nhớ đệm của MySQL. |
| **`nginx-exporter`** | `nginx_exporter` | `nginx/nginx-prometheus-exporter` | 9113 | *Không mở* | Thu thập lưu lượng request từ `/stub_status` của Nginx. |
| **`prometheus`**| `prometheus_monitoring`| `prom/prometheus:latest` | 9090 | **9090** | Time-series Database thu thập và lưu trữ toàn bộ Metrics. |
| **`grafana`** | `grafana_dashboard` | `grafana/grafana:latest` | 3000 | **3001** | Bảng điều khiển trực quan hóa Metrics và LogQL. |
| **`loki`** | `loki_logger` | `grafana/loki:latest` | 3100 | **3100** | Hệ thống lưu trữ và đánh chỉ mục Log tập trung. |
| **`promtail`** | `promtail_agent` | `grafana/promtail:latest` | 9080 | *Không mở* | Agent đọc file log Nginx và đẩy dữ liệu về Loki. |

### 2.3. Thiết kế luồng mạng và Phân vùng mạng (Network Isolation)
Để thực hiện tiêu chí **Hardening**, hệ thống được chia làm 2 phân vùng mạng bridge độc lập:
1. **`frontend-net`:** Dành cho các dịch vụ tiếp nhận kết nối bên ngoài và hệ thống quản trị giám sát (`nginx`, `wordpress`, `phpmyadmin`, `prometheus`, `grafana`, `loki`, `promtail`, `cadvisor`, `nginx-exporter`).
2. **`backend-net`:** Vùng mạng nội bộ cô lập chứa `db` (MySQL 8.0), `wordpress`, `phpmyadmin` và `mysqld-exporter`.
* **Ý nghĩa an ninh:** Cổng kết nối MySQL (3306) hoàn toàn **không được public ra máy chủ host**. Kẻ tấn công từ bên ngoài không thể scan port hay tấn công Brute-force mật khẩu database trực tiếp.

---

\newpage

# CHƯƠNG 3: TRIỂN KHAI ỨNG DỤNG WEB, CSDL VÀ NGINX REVERSE PROXY (COMMIT 1)

### 3.1. Cấu hình CSDL MySQL 8.0 và phpMyAdmin
* Dữ liệu MySQL được lưu trữ bền vững trên **Docker Volume** mang tên `db_data` ánh xạ vào `/var/lib/mysql`.
* Biến môi trường kết nối được đồng bộ qua file `.env`:
  ```env
  MYSQL_ROOT_PASSWORD=SuperSecurePassword123!
  MYSQL_DATABASE=wordpress_db
  MYSQL_USER=wordpress_user
  MYSQL_PASSWORD=SecureUserPassword2026!
  ```
* phpMyAdmin được cấu hình biến `PMA_ABSOLUTE_URI: https://localhost/phpmyadmin/` để xử lý chuẩn xác đường dẫn CSS/JS và phiên làm việc khi chạy phía sau Reverse Proxy.

### 3.2. Cấu hình Web Application WordPress (Showroom TechStore)
* Sử dụng Image chính thức `wordpress:latest`.
* Để ngăn chặn lỗi vòng lặp chuyển hướng HTTPS (`ERR_TOO_MANY_REDIRECTS`), cấu hình `WORDPRESS_CONFIG_EXTRA` được thiết lập:
  ```php
  define('WP_HOME', 'https://localhost');
  define('WP_SITEURL', 'https://localhost');
  define('FORCE_SSL_ADMIN', true);
  $_SERVER['HTTPS'] = 'on';
  ```
* **Dữ liệu Demo sản phẩm:** Ứng dụng đã được kích hoạt Theme **Astra** và nạp 4 bài viết quảng bá sản phẩm công nghệ hoàn chỉnh (ASUS ROG Zephyrus G16, iPhone 16 Pro Max, Tai nghe Sony WH-1000XM5, Bàn phím Keychron Q1 Pro).

### 3.3. Cấu hình Nginx Reverse Proxy và Chứng chỉ số SSL/TLS tự ký
* Chứng chỉ số tự ký được sinh ra bằng OpenSSL với thời hạn 365 ngày (`nginx.crt` và `nginx.key`).
* File `nginx.conf` thực hiện chuyển hướng toàn bộ traffic HTTP (Port 80) sang HTTPS (Port 443) với mã trạng thái `301 Moved Permanently`.
* Cấu hình 5 Security Headers bảo vệ ứng dụng:
  ```nginx
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header X-XSS-Protection "1; mode=block" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header Referrer-Policy "no-referrer-when-downgrade" always;
  add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:;" always;
  ```

### 3.4. Minh chứng kết quả triển khai Chương 3

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 3.1: CHÈN ẢNH CHỤP GIAO DIỆN TRANG CHỦ WORDPRESS CHẠY TRÊN HTTPS TẠI ĐÂY]  │
│ (Mô tả: Giao diện Showroom TechStore với các sản phẩm demo và ổ khóa SSL xanh)  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 3.2: CHÈN ẢNH CHỤP GIAO DIỆN PHPMYADMIN ĐĂNG NHẬP THÀNH CÔNG TẠI ĐÂY]     │
│ (Mô tả: Giao diện phpMyAdmin tại https://localhost/phpmyadmin/ quản lý CSDL)    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 3.3: CHÈN ẢNH CHỤP CHI TIẾT CHỨNG CHỈ SỐ SSL TỰ KÝ TRÊN TRÌNH DUYỆT]       │
│ (Mô tả: Cửa sổ Certificate Viewer hiển thị thời hạn và thuật toán mã hóa SHA-256)│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

\newpage

# CHƯƠNG 4: HỆ THỐNG GIÁM SÁT HIỆU NĂNG PROMETHEUS VÀ GRAFANA (COMMIT 2)

### 4.1. Nguyên lý hoạt động của Prometheus và các Exporter
Prometheus hoạt động theo cơ chế **Pull Model**: Cứ định kỳ 15 giây (`scrape_interval: 15s`), Prometheus gửi HTTP GET request đến endpoint `/metrics` của các Exporter để thu thập số liệu time-series dưới dạng các cặp `Metric_Name{labels} Value`.

### 4.2. Cấu hình cAdvisor (Container Monitoring)
* `cAdvisor` truy cập trực tiếp vào Docker Daemon socket `/var/run/docker.sock` và cgroups của nhân Linux để đo đạc chính xác mức độ chiếm dụng CPU, RAM, Network I/O của từng container.
* Metric tiêu biểu: `container_cpu_usage_seconds_total`, `container_memory_usage_bytes`.

### 4.3. Cấu hình mysqld-exporter (Database Monitoring)
* `mysqld-exporter` kết nối an toàn vào MySQL qua tài khoản `wordpress_user` trên cổng 3306 nội bộ.
* Metric tiêu biểu: `mysql_global_status_uptime`, `mysql_global_status_threads_connected`, `mysql_global_status_questions`.

### 4.4. Cấu hình nginx-prometheus-exporter (Web Server Monitoring)
* Nginx mở endpoint nội bộ `location /stub_status` để cung cấp số liệu kết nối active. Exporter cào dữ liệu và chuyển đổi thành định dạng Prometheus.
* Metric tiêu biểu: `nginx_connections_active`, `nginx_connections_handled`.

### 4.5. Tự động hóa Dashboard trực quan hóa trên Grafana
Hệ thống sử dụng cơ chế **Grafana Provisioning** (`datasources.yaml` và `dashboards.yaml`) giúp tự động nạp nguồn dữ liệu Prometheus và thiết lập Dashboard chuyên nghiệp mang tên **"Hệ Thống Giám Sát Container & Máy Chủ - DTC245200425"**.

### 4.6. Minh chứng kết quả triển khai Chương 4

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 4.1: CHÈN ẢNH CHỤP MÀN HÌNH PROMETHEUS TARGETS (HTTP://LOCALHOST:9090)]    │
│ (Mô tả: Cả 4 Targets: cadvisor, mysql, nginx, prometheus đều hiển thị màu xanh UP) │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 4.2: CHÈN ẢNH CHỤP DASHBOARD GIÁM SÁT TRÊN GRAFANA (HTTP://LOCALHOST:3001)] │
│ (Mô tả: Các biểu đồ sóng CPU %, Dung lượng RAM, MySQL Queries/s và Nginx Traffic)│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

\newpage

# CHƯƠNG 5: HỆ THỐNG QUẢN LÝ NHẬT KÝ TẬP TRUNG LOKI VÀ PROMTAIL (COMMIT 3)

### 5.1. Kiến trúc thu thập log với Promtail và lưu trữ trên Loki
Khác với mô hình ELK (Elasticsearch) cồng kềnh, **Grafana Loki** được thiết kế theo triết lý tối giản: chỉ đánh chỉ mục (index) các siêu dữ liệu (Labels) thay vì toàn bộ nội dung log, giúp tiết kiệm bộ nhớ RAM và dung lượng lưu trữ đáng kể.

### 5.2. Cấu hình pipeline đọc log Nginx
* Thư mục log của Nginx được đồng bộ ra thư mục chia sẻ `./nginx/logs:/var/log/nginx`.
* Agent **Promtail** giám sát tập tin `/var/log/nginx/*.log`, gắn nhãn `{job="nginx"}` và đẩy dữ liệu (Push) qua HTTP tới endpoint của Loki tại `http://loki:3100/loki/api/v1/push`.

### 5.3. Xây dựng và thực thi các câu truy vấn LogQL thực tế

Trong giao diện **Grafana Explore**, sinh viên đã thiết lập và thực thi 3 câu truy vấn LogQL phục vụ điều tra sự cố:

1. **Truy vấn toàn bộ log truy cập của hệ thống:**
   ```logql
   {job="nginx"}
   ```
   *Ý nghĩa:* Xem toàn bộ lịch sử các request của khách hàng gửi tới Nginx.

2. **Truy vấn lọc các truy cập gặp mã lỗi HTTP (4xx Client Error hoặc 5xx Server Error):**
   ```logql
   {job="nginx"} |~ " (4[0-9]{2}|5[0-9]{2}) "
   ```
   *Ý nghĩa:* Giúp quản trị viên phát hiện ngay các lỗi truy cập trang không tồn tại (404) hoặc lỗi sập ứng dụng (500/502).

3. **Truy vấn tính toán tần suất request theo thời gian (Request Rate):**
   ```logql
   rate({job="nginx"}[1m])
   ```
   *Ý nghĩa:* Thống kê lưu lượng truy cập theo từng phút để phát hiện hiện tượng bất thường hoặc tấn công từ chối dịch vụ (DDoS).

### 5.4. Minh chứng kết quả triển khai Chương 5

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 5.1: CHÈN ẢNH CHỤP GRAFANA EXPLORE TRUY VẤN LOGQL THÀNH CÔNG TẠI ĐÂY]     │
│ (Mô tả: Màn hình hiển thị câu lệnh {job="nginx"} và danh sách các dòng log Nginx)│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

\newpage

# CHƯƠNG 6: CÁC GIẢI PHÁP BẢO MẬT (HARDENING) VÀ QUẢN LÝ MÃ NGUỒN GITHUB

### 6.1. Phân tích các giải pháp Hardening đã áp dụng

Hệ thống đã triển khai toàn diện **4 biện pháp bảo mật (Hardening)** then chốt:

1. **Cách ly mạng (Network Isolation):**
   * Thiết lập 2 phân vùng mạng bridge riêng biệt. Cơ sở dữ liệu MySQL chỉ nằm ở `backend-net`, hoàn toàn ẩn giấu cổng 3306 khỏi mạng Internet.
2. **Quyền truy cập chỉ đọc (Read-Only Mounts):**
   * Các tệp cấu hình quan trọng (`nginx.conf`, `prometheus.yml`, `promtail-config.yml`) và cặp khóa SSL (`nginx.crt`, `nginx.key`) được mount vào container với cờ `:ro` (Read-Only). Ngay cả khi container bị tấn công chiếm quyền, mã độc cũng không thể ghi đè hay sửa đổi cấu hình hệ thống.
3. **Bảo vệ ứng dụng bằng HTTP Security Headers:**
   * Nginx được cấu hình đầy đủ `X-Frame-Options` (chống Clickjacking), `X-Content-Type-Options` (chống MIME Sniffing), `X-XSS-Protection` và `Content-Security-Policy`.
4. **Nguyên tắc phân quyền tối thiểu (Least Privilege) cho Database:**
   * Thay vì sử dụng quyền `root` cho mọi thao tác, `mysqld-exporter` và `wordpress` được cấp tài khoản người dùng riêng biệt `wordpress_user` với quyền hạn giới hạn trong phạm vi CSDL `wordpress_db`.

### 6.2. Quản lý cấu hình bí mật qua Biến môi trường (.env)
* Toàn bộ mật khẩu nhạy cảm (`MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`) được lưu trữ tại file `.env`.
* File `.env` được khai báo trong `.gitignore` để không bao giờ bị đẩy lên GitHub.
* Dự án cung cấp file `.env.example` làm mẫu cấu hình an toàn cho người sử dụng khác.

### 6.3. Quản lý mã nguồn theo chuẩn Git Workflow trên GitHub
* **Tên Repository:** Đặt chuẩn theo Mã số sinh viên: `DTC245200425`.
* **Lịch sử Commit rõ ràng theo từng mốc tiến độ:**
  * `Commit 1:` Add Nginx reverse proxy with HTTPS self-signed and security headers.
  * `Commit 2:` Setup Prometheus, Exporters, and Grafana for monitoring.
  * `Commit 3:` Add Loki, Promtail centralized logging and system hardening.
  * `Commit 4 & 5:` Optimize docker-compose, fix queries, add provisioning and documentation.

### 6.4. Minh chứng kết quả triển khai Chương 6

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 6.1: CHÈN ẢNH CHỤP LỊCH SỬ COMMIT TRÊN GITHUB REPOSITORY TẠI ĐÂY]          │
│ (Mô tả: Lịch sử các Commit rõ ràng tại https://github.com/maidangcuong/DTC245200425) │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [HÌNH 6.2: CHÈN ẢNH CHỤP LỆNH DOCKER COMPOSE PS HIỂN THỊ CÁC CONTAINER RUNNING]   │
│ (Mô tả: Màn hình Terminal hiển thị đầy đủ 10 containers đều ở trạng thái UP)    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

\newpage

# CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 7.1. Đánh giá kết quả đạt được
Sau quá trình nghiên cứu và thực hiện đề tài số 03, sinh viên đã hoàn thành 100% các mục tiêu đề ra:
* Xây dựng thành công hệ thống Website Quảng bá Sản phẩm WordPress trên nền tảng Docker Compose hoạt động ổn định, mượt mà.
* Làm chủ kỹ thuật cấu hình Nginx Reverse Proxy, mã hóa SSL/TLS và triển khai các tiêu chuẩn bảo mật Hardening thực tế.
* Tích hợp hoàn chỉnh hệ sinh thái giám sát hiện đại gồm Prometheus, 3 bộ Exporters chuyên dụng và Grafana Dashboard trực quan.
* Triển khai giải pháp gom log tập trung với Grafana Loki và Promtail, làm chủ kỹ năng truy vấn LogQL phục vụ vận hành và xử lý sự cố.
* Quản lý mã nguồn chuyên nghiệp trên GitHub, tuân thủ đúng quy chuẩn đặt tên và hướng dẫn vận hành trong README.md.

### 7.2. Bài học kinh nghiệm
* Hiểu sâu sắc về cơ chế hoạt động của Containerization, Docker Network, Volume Binding và sự khác biệt giữa các mô hình mạng.
* Nắm vững nguyên lý hoạt động của kiến trúc Pull (Prometheus) và Push (Loki/Promtail) trong hệ thống Observability.
* Rèn luyện kỹ năng khắc phục sự cố (Troubleshooting) khi xử lý các lỗi thường gặp trong môi trường phân tán như lỗi vòng lặp chuyển hướng SSL (ERR_TOO_MANY_REDIRECTS), lỗi phân quyền MySQL 8.0 và lỗi lọc nhãn cAdvisor trên môi trường ảo hóa WSL2.

### 7.3. Hướng phát triển trong tương lai
* Tích hợp hệ thống cảnh báo tự động qua **Prometheus Alertmanager** gửi thông báo về Telegram / Slack khi CPU/RAM vượt ngưỡng 85% hoặc khi phát sinh nhiều lỗi HTTP 500.
* Nâng cấp hạ tầng từ Docker Compose đơn lẻ lên cụm điều phối container chuyên nghiệp **Kubernetes (K8s)** để tự động mở rộng (Auto-scaling) và tăng tính sẵn sàng cao (High Availability).
* Tích hợp hệ thống chứng chỉ số tự động gia hạn thông qua **Let's Encrypt** và Certbot cho môi trường Production thực tế.

---

\newpage

# TÀI LIỆU THAM KHẢO

1. **Docker Documentation:** *Docker Compose file reference and best practices for production* - [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
2. **Nginx Official Docs:** *Reverse Proxy setup, SSL Termination, and Security Headers* - [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
3. **Prometheus Documentation:** *Prometheus Overview, Metrics types, and PromQL basics* - [https://prometheus.io/docs/](https://prometheus.io/docs/)
4. **Grafana Labs:** *Grafana Loki Documentation & LogQL Query Language Reference* - [https://grafana.com/docs/loki/latest/](https://grafana.com/docs/loki/latest/)
5. **OWASP Foundation:** *OWASP Secure Headers Project & REST Security Cheat Sheet* - [https://owasp.org/www-project-secure-headers/](https://owasp.org/www-project-secure-headers/)
6. **WordPress Developer Resources:** *Configuring WordPress behind Reverse Proxies and SSL* - [https://developer.wordpress.org/](https://developer.wordpress.org/)
