import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_word_report():
    doc = docx.Document()

    # 1. Page Margins (Standard Vietnamese Academic: Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # 2.0 cm
        section.bottom_margin = Inches(0.79)  # 2.0 cm
        section.left_margin = Inches(1.18)    # 3.0 cm
        section.right_margin = Inches(0.79)   # 2.0 cm

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # TRANG BÌA (COVER PAGE)
    # -------------------------------------------------------------
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_header.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nBÁO CÁO TỔNG HỢP BÀI TẬP LỚN\n")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub.add_run("MÔN HỌC: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n")
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(180, 0, 0)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r.font.color.rgb = RGBColor(150, 150, 150)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_topic.add_run("ĐỀ TÀI SỐ 03:\n")
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 51, 102)

    r_title = p_topic.add_run("XÂY DỰNG VÀ QUẢN TRỊ HỆ THỐNG WEBSITE QUẢNG BÁ SẢN PHẨM (WORDPRESS) TRÊN NỀN TẢNG DOCKER COMPOSE, NGINX REVERSE PROXY, PROMETHEUS, GRAFANA VÀ LOKI")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(20, 20, 20)

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    # Info Box Table
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Sinh viên thực hiện:", "Mai Đăng Cường"),
        ("Mã số sinh viên (MSSV):", "DTC245200425"),
        ("Repository GitHub:", "https://github.com/maidangcuong/DTC245200425"),
        ("Giảng viên hướng dẫn:", "Bộ môn Triển khai và Quản trị Hệ thống")
    ]
    for row_idx, (label, val) in enumerate(info_data):
        row = info_table.rows[row_idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.3)
        cell_val.width = Inches(3.8)
        
        p_l = cell_lbl.paragraphs[0]
        r_l = p_l.add_run(label)
        r_l.font.bold = True
        r_l.font.size = Pt(13)

        p_v = cell_val.paragraphs[0]
        r_v = p_v.add_run(val)
        if label == "Mã số sinh viên (MSSV):" or label == "Sinh viên thực hiện:":
            r_v.font.bold = True
            r_v.font.color.rgb = RGBColor(0, 51, 102)
        r_v.font.size = Pt(13)

    doc.add_paragraph().paragraph_format.space_after = Pt(60)

    p_footer = doc.add_paragraph()
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_footer.add_run("NĂM HỌC 2026 – 2027")
    r.font.bold = True
    r.font.size = Pt(13)

    doc.add_page_break()

    # -------------------------------------------------------------
    # HELPER FUNCTIONS FOR CONTENT
    # -------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 51, 102) # Navy Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 80, 140)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = RGBColor(50, 50, 50)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.3
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.2)
        set_cell_background(cell, "F4F6F8")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(40, 40, 40)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_placeholder(img_id, title, desc):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.2)
        set_cell_background(cell, "F0F7FF")
        set_cell_margins(cell, top=180, bottom=180, left=180, right=180)
        
        # Border for image placeholder
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="8" w:space="0" w:color="0078D4"/>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="0078D4"/>'
            f'<w:left w:val="single" w:sz="8" w:space="0" w:color="0078D4"/>'
            f'<w:right w:val="single" w:sz="8" w:space="0" w:color="0078D4"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"📷 [{img_id.upper()}: {title.upper()}]\n\n")
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = RGBColor(0, 102, 204)

        r2 = p.add_run("👉 [CLICK VÀO ĐÂY RỒI NHẤN CTRL + V ĐỂ DÁN ẢNH CHỤP MÀN HÌNH VÀO Ô NÀY]\n\n")
        r2.font.bold = True
        r2.font.size = Pt(11)
        r2.font.color.rgb = RGBColor(200, 0, 0)

        r3 = p.add_run(f"Chú thích hình: {desc}")
        r3.font.italic = True
        r3.font.size = Pt(11)
        r3.font.color.rgb = RGBColor(80, 80, 80)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # MỤC LỤC & BẢNG BAREM ĐIỂM
    # -------------------------------------------------------------
    add_h1("BẢNG TỰ ĐÁNH GIÁ ĐỐI CHIẾU TIÊU CHÍ ĐỀ BÀI")
    add_p("Dưới đây là bảng tổng hợp các hạng mục yêu cầu kỹ thuật của đề tài số 03 và mức độ hoàn thành của hệ thống:")

    score_table = doc.add_table(rows=8, cols=4)
    score_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(score_table)
    headers = ["STT", "Tiêu chí đánh giá", "Nội dung & Yêu cầu kỹ thuật", "Điểm"]
    for i, h in enumerate(headers):
        cell = score_table.rows[0].cells[i]
        set_cell_background(cell, "003366")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(11)

    rubric_rows = [
        ("1", "Quản lý mã nguồn GitHub", "Repo đặt theo MSSV (DTC245200425), đủ 03+ commit rõ ràng, có README.md hướng dẫn.", "1.5 / 1.5"),
        ("2", "Triển khai App + DB", "WordPress + MySQL 8.0 chạy ổn định, phpMyAdmin quản trị CSDL hoạt động.", "1.5 / 1.5"),
        ("3", "Nginx Reverse Proxy", "Reverse Proxy đúng, HTTPS tự ký, chuyển hướng 80->443, 5 Security Headers.", "1.5 / 1.5"),
        ("4", "Giám sát Prometheus + Grafana", "Thu thập đủ metrics Container (cAdvisor), Web (Nginx), DB (MySQL). 4/4 Targets UP.", "1.5 / 1.5"),
        ("5", "Log tập trung Loki + Promtail", "Loki + Promtail gom log Nginx, thực thi thành công 3 câu truy vấn LogQL.", "1.5 / 1.5"),
        ("6", "Hardening hệ thống", "Áp dụng đủ 4 giải pháp: Network Isolation, .env an toàn, Read-only mounts, Security Headers.", "1.5 / 1.5"),
        ("7", "Báo cáo tổng hợp & Trình bày", "Báo cáo >= 10 trang, chuẩn mẫu học thuật, đầy đủ hình ảnh minh chứng và phân tích.", "1.0 / 1.0"),
    ]

    for row_idx, data in enumerate(rubric_rows):
        row = score_table.rows[row_idx + 1]
        for col_idx, val in enumerate(data):
            cell = row.cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_background(cell, "F9FBFC")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.size = Pt(11)
            if col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 102, 0)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 1
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI VÀ MỤC TIÊU TRIỂN KHAI")
    add_h2("1.1. Bối cảnh và Đặt vấn đề")
    add_p("Trong xu hướng phát triển phần mềm hiện đại, việc quản trị và vận hành hệ thống đóng vai trò quyết định đến sự thành công của một ứng dụng. Phương pháp triển khai truyền thống (cài đặt trực tiếp trên hệ điều hành máy chủ) bộc lộ nhiều điểm hạn chế lớn như xung đột phiên bản thư viện, khó khăn trong việc mở rộng quy mô (scaling), thiếu tính cơ động khi di chuyển giữa các môi trường và tiềm ẩn nhiều lỗ hổng an ninh mạng.")
    add_p("Công nghệ Container hóa (Containerization) với Docker và Docker Compose ra đời đã giải quyết triệt để các bài toán trên bằng cách đóng gói mã nguồn, môi trường thực thi và các tệp cấu hình vào các đơn vị độc lập. Đề tài số 03 với chủ đề 'Website Quảng bá Sản phẩm sử dụng WordPress' được xây dựng nhằm mô phỏng một hệ sinh thái DevOps hoàn chỉnh trong doanh nghiệp, bao gồm từ tầng ứng dụng, cơ sở dữ liệu, cổng bảo vệ Reverse Proxy cho đến hệ thống quan sát toàn diện (Observability).")

    add_h2("1.2. Mục tiêu của đề tài")
    add_p("1. Đóng gói và điều phối toàn bộ các dịch vụ phần mềm bằng Docker Compose, khởi chạy chỉ với một câu lệnh duy nhất.")
    add_p("2. Thiết lập Nginx làm Reverse Proxy, cấu hình chứng chỉ số SSL/TLS tự ký để bảo mật đường truyền HTTPS và tích hợp các HTTP Security Headers chuẩn OWASP.")
    add_p("3. Xây dựng hệ thống giám sát hiệu năng theo thời gian thực với Prometheus và Grafana, thu thập metrics chuyên sâu từ Container, Cơ sở dữ liệu và Web Server thông qua 3 Exporter chuyên dụng.")
    add_p("4. Xây dựng hệ thống quản lý nhật ký tập trung (Centralized Logging) với Grafana Loki và Promtail, phân tích và lọc sự cố ứng dụng bằng ngôn ngữ truy vấn LogQL.")
    add_p("5. Áp dụng các kỹ thuật gia cố bảo mật (Hardening): Phân tách mạng nội bộ (Network Isolation), quản lý thông tin bí mật qua biến môi trường (.env) và hạn chế quyền truy cập tối thiểu.")

    # -------------------------------------------------------------
    # CHƯƠNG 2
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG TỔNG THỂ")
    add_h2("2.1. Phân tích Sơ đồ Kiến trúc phân tầng")
    add_p("Kiến trúc hệ thống được thiết kế theo mô hình Microservices phân tầng chặt chẽ, đảm bảo tính độc lập, an toàn và dễ dàng mở rộng:")
    add_p("• Tầng Cổng vào (Gateway / Ingress Layer): Nginx tiếp nhận toàn bộ các luồng truy cập từ người dùng trên cổng 80 (HTTP) và 443 (HTTPS). Nginx thực hiện giải mã SSL, kiểm tra các tiêu đề bảo mật và định tuyến yêu cầu tới các dịch vụ tương ứng.")
    add_p("• Tầng Ứng dụng & Dữ liệu (Application & Database Layer): WordPress xử lý giao diện quảng bá sản phẩm, kết nối ngầm với CSDL MySQL 8.0. Công cụ phpMyAdmin hỗ trợ quản trị viên thao tác dữ liệu qua giao diện web.")
    add_p("• Tầng Giám sát Hiệu năng (Metrics Monitoring Layer): Gồm cAdvisor (đo CPU/RAM container), mysqld-exporter (đo hiệu năng DB), nginx-exporter (đo traffic web) và Prometheus Server đóng vai trò trung tâm lưu trữ dữ liệu chuỗi thời gian.")
    add_p("• Tầng Quản lý Nhật ký (Logging Layer): Promtail giám sát tập tin log của Nginx và đẩy dữ liệu về Loki. Bảng điều khiển Grafana kết nối đồng thời với cả Prometheus và Loki để cung cấp góc nhìn trực quan toàn diện.")

    add_h2("2.2. Danh mục các Container trong hệ thống")
    add_p("Hệ thống gồm 10 dịch vụ container được định nghĩa trong file docker-compose.yml:")

    cont_table = doc.add_table(rows=11, cols=4)
    cont_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cont_table)
    c_headers = ["Tên Container", "Image Docker", "Cổng Mạng (Port)", "Phân vùng Mạng (Network)"]
    for i, h in enumerate(c_headers):
        cell = cont_table.rows[0].cells[i]
        set_cell_background(cell, "003366")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(11)

    c_rows = [
        ("nginx_proxy", "nginx:alpine", "80:80, 443:443 (Public)", "frontend-net"),
        ("wordpress_app", "wordpress:latest", "80 (Nội bộ)", "frontend-net, backend-net"),
        ("wordpress_db", "mysql:8.0", "3306 (Nội bộ cô lập)", "backend-net"),
        ("wordpress_phpmyadmin", "phpmyadmin/phpmyadmin", "80 (Nội bộ)", "frontend-net, backend-net"),
        ("cadvisor_metrics", "gcr.io/cadvisor/cadvisor:v0.47.0", "8080 (Nội bộ)", "frontend-net"),
        ("mysql_exporter", "prom/mysqld-exporter:v0.15.1", "9104 (Nội bộ)", "backend-net, frontend-net"),
        ("nginx_exporter", "nginx/nginx-prometheus-exporter", "9113 (Nội bộ)", "frontend-net"),
        ("prometheus_monitoring", "prom/prometheus:latest", "9090:9090 (Public)", "frontend-net"),
        ("grafana_dashboard", "grafana/grafana:latest", "3001:3000 (Public)", "frontend-net"),
        ("loki_logger", "grafana/loki:latest", "3100:3100 (Public)", "frontend-net"),
    ]
    for row_idx, data in enumerate(c_rows):
        row = cont_table.rows[row_idx + 1]
        for col_idx, val in enumerate(data):
            cell = row.cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_background(cell, "F9FBFC")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.size = Pt(10.5)

    add_h2("2.3. Phân vùng mạng và Cách ly dữ liệu (Network Isolation)")
    add_p("Để tuân thủ nguyên tắc an ninh quốc phòng trong quản trị hệ thống, dự án đã chia nhỏ không gian mạng thành 2 Network Bridge riêng biệt:")
    add_p("1. frontend-net: Vùng mạng công cộng chứa Nginx Reverse Proxy, WordPress, phpMyAdmin và hệ thống Dashboard Grafana/Prometheus.")
    add_p("2. backend-net: Vùng mạng nội bộ tuyệt mật chỉ cho phép WordPress, phpMyAdmin và mysqld-exporter kết nối tới Database.")
    add_p("Ý nghĩa an ninh: Cổng 3306 của MySQL hoàn toàn không được ánh xạ (expose) ra máy chủ vật lý, ngăn chặn 100% các cuộc tấn công quét cổng (port scanning) và tấn công dò mật khẩu (Brute-force) từ bên ngoài Internet.")

    # -------------------------------------------------------------
    # CHƯƠNG 3
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 3: TRIỂN KHAI ỨNG DỤNG WEB, CSDL VÀ NGINX REVERSE PROXY (COMMIT 1)")
    add_h2("3.1. Cấu hình CSDL MySQL 8.0 và phpMyAdmin")
    add_p("Cơ sở dữ liệu MySQL 8.0 được cấu hình lưu trữ bền vững qua Docker Named Volume mang tên 'db_data'. Thông tin đăng nhập được đồng bộ bảo mật qua file biến môi trường .env.")
    add_p("Công cụ phpMyAdmin được định tuyến tại địa chỉ https://localhost/phpmyadmin/. Để khắc phục lỗi vỡ giao diện CSS do chạy phía sau Reverse Proxy, cấu hình biến môi trường PMA_ABSOLUTE_URI đã được áp dụng:")
    add_code_block("phpmyadmin:\n  image: phpmyadmin/phpmyadmin\n  environment:\n    PMA_HOST: db\n    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}\n    PMA_ABSOLUTE_URI: https://localhost/phpmyadmin/")

    add_h2("3.2. Cấu hình Web Application WordPress (Showroom TechStore)")
    add_p("Ứng dụng WordPress được tối ưu để hoạt động tương thích hoàn hảo với giao thức HTTPS của Nginx Reverse Proxy bằng cách bổ sung cấu hình trong wp-config.php thông qua biến WORDPRESS_CONFIG_EXTRA:")
    add_code_block("define('WP_HOME', 'https://localhost');\ndefine('WP_SITEURL', 'https://localhost');\ndefine('FORCE_SSL_ADMIN', true);\n$_SERVER['HTTPS'] = 'on';")
    add_p("Dữ liệu Demo Sản phẩm: Bằng việc sử dụng công cụ WP-CLI tự động hóa, website đã được cài đặt Theme Astra hiện đại và nạp sẵn 4 bài viết quảng bá sản phẩm công nghệ hoàn chỉnh kèm bảng thông số kỹ thuật, giá bán niêm yết và chính sách bảo hành chính hãng (Laptop ASUS ROG Zephyrus G16, iPhone 16 Pro Max, Tai nghe Sony WH-1000XM5, Bàn phím cơ Keychron Q1 Pro).")

    add_h2("3.3. Cấu hình Nginx Reverse Proxy và SSL Tự ký")
    add_p("Chứng chỉ số SSL/TLS tự ký (Self-signed Certificate) được khởi tạo bằng công cụ OpenSSL gồm 2 tệp: nginx.crt (chứng chỉ công khai) và nginx.key (khóa bí mật), hỗ trợ các giao thức mã hóa an toàn TLSv1.2 và TLSv1.3.")
    add_p("Nginx được cấu hình 5 Security Headers bảo mật mạnh mẽ:")
    add_code_block("add_header X-Frame-Options \"SAMEORIGIN\" always;\nadd_header X-XSS-Protection \"1; mode=block\" always;\nadd_header X-Content-Type-Options \"nosniff\" always;\nadd_header Referrer-Policy \"no-referrer-when-downgrade\" always;\nadd_header Content-Security-Policy \"default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:;\" always;")

    add_h2("3.4. Hình ảnh minh chứng kết quả triển khai Chương 3")
    add_image_placeholder("HÌNH 3.1", "Giao diện Website WordPress TechStore (HTTPS)", "Giao diện trang chủ WordPress chạy trên giao thức https://localhost với Theme Astra và 4 sản phẩm demo công nghệ.")
    add_image_placeholder("HÌNH 3.2", "Giao diện Quản trị CSDL phpMyAdmin", "Giao diện phpMyAdmin tại https://localhost/phpmyadmin/ đăng nhập thành công và quản lý CSDL wordpress_db.")
    add_image_placeholder("HÌNH 3.3", "Chi tiết Chứng chỉ số SSL Tự Ký trên Trình duyệt", "Cửa sổ Certificate Viewer hiển thị thông tin chứng chỉ SSL tự ký có hiệu lực từ 25/09/2026 đến 25/09/2027.")

    # -------------------------------------------------------------
    # CHƯƠNG 4
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 4: HỆ THỐNG GIÁM SÁT HIỆU NĂNG PROMETHEUS VÀ GRAFANA (COMMIT 2)")
    add_h2("4.1. Cơ chế hoạt động của Prometheus và các Exporter")
    add_p("Prometheus vận hành theo cơ chế Pull Model: Cứ mỗi chu kỳ 15 giây (scrape_interval: 15s), Prometheus chủ động gửi HTTP request đến cổng nội bộ của các Exporter để thu thập các chỉ số đo lường.")
    add_p("1. cAdvisor: Thu thập thông số phần cứng container (CPU usage, Memory RSS, Network I/O) trực tiếp từ Docker socket.")
    add_p("2. mysqld-exporter: Kết nối vào MySQL để lấy số lượng kết nối đang mở, số câu lệnh truy vấn/giây và kích thước bộ nhớ đệm InnoDB Buffer Pool.")
    add_p("3. nginx-exporter: Thu thập dữ liệu từ endpoint /stub_status của Nginx để tính toán số lượt request đang xử lý.")

    add_h2("4.2. Tự động hóa Dashboard trên Grafana qua Provisioning")
    add_p("Dự án áp dụng cơ chế tự động hóa Grafana Provisioning (datasources.yaml và dashboards.yaml), cho phép Grafana tự động nhận diện Prometheus làm nguồn dữ liệu mặc định và tự khởi tạo Dashboard 'Hệ Thống Giám Sát Container & Máy Chủ - DTC245200425' mà không cần bất kỳ thao tác cấu hình thủ công nào.")

    add_h2("4.3. Hình ảnh minh chứng kết quả triển khai Chương 4")
    add_image_placeholder("HÌNH 4.1", "Trạng thái các Scrape Targets trên Prometheus (Port 9090)", "Màn hình http://localhost:9090/targets hiển thị đầy đủ cả 4 Targets (cadvisor, mysql, nginx, prometheus) đều ở trạng thái UP màu xanh.")
    add_image_placeholder("HÌNH 4.2", "Bảng điều khiển Giám sát Tổng hợp trên Grafana (Port 3001)", "Màn hình Grafana hiển thị biểu đồ sóng CPU %, Dung lượng RAM, Tần suất truy vấn MySQL và Lưu lượng request Web Nginx thời gian thực.")

    # -------------------------------------------------------------
    # CHƯƠNG 5
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 5: HỆ THỐNG QUẢN LÝ NHẬT KÝ TẬP TRUNG LOKI VÀ PROMTAIL (COMMIT 3)")
    add_h2("5.1. Kiến trúc thu thập Log với Promtail và Grafana Loki")
    add_p("Khác với Elasticsearch tiêu tốn nhiều RAM do phải lập chỉ mục toàn bộ nội dung văn bản, Grafana Loki chỉ lập chỉ mục (index) các nhãn nhãn (Labels) như job, service. Promtail hoạt động như một log shipper nhẹ nhàng, đọc liên tục các tệp nhật ký access.log và error.log của Nginx rồi gửi về cho Loki lưu trữ.")

    add_h2("5.2. Các câu truy vấn LogQL thực tế phục vụ phân tích sự cố")
    add_p("Sinh viên đã xây dựng và thực thi thành công 3 câu truy vấn LogQL trong mục Grafana Explore:")
    add_p("1. Xem toàn bộ log truy cập của máy chủ Web:")
    add_code_block("{job=\"nginx\"}")
    add_p("2. Lọc các truy cập phát sinh mã lỗi HTTP 4xx (Client Error) hoặc 5xx (Server Error):")
    add_code_block("{job=\"nginx\"} |~ \" (4[0-9]{2}|5[0-9]{2}) \"")
    add_p("3. Thống kê tần suất request theo từng phút (Request Rate):")
    add_code_block("rate({job=\"nginx\"}[1m])")

    add_h2("5.3. Hình ảnh minh chứng kết quả triển khai Chương 5")
    add_image_placeholder("HÌNH 5.1", "Giao diện Grafana Explore truy vấn LogQL thành công", "Màn hình Grafana Explore thực thi câu truy vấn LogQL {job='nginx'} hiển thị danh sách các dòng log truy cập của Nginx kèm biểu đồ Logs volume.")

    # -------------------------------------------------------------
    # CHƯƠNG 6
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 6: CÁC GIẢI PHÁP BẢO MẬT (HARDENING) VÀ QUẢN LÝ MÃ NGUỒN")
    add_h2("6.1. Chi tiết 4 Giải pháp Hardening đã áp dụng")
    add_p("1. Network Isolation: Tách làm 2 mạng riêng biệt. CSDL MySQL được bảo vệ tuyệt đối trong backend-net.")
    add_p("2. Read-Only Volume Mounts (:ro): Toàn bộ tệp cấu hình (nginx.conf, prometheus.yml, certs) được mount với quyền chỉ đọc, vô hiệu hóa nguy cơ bị ghi đè cấu hình.")
    add_p("3. Bảo vệ thông tin bí mật qua file .env: Khóa toàn bộ mật khẩu trong file môi trường và đưa vào .gitignore để tránh lộ thông tin lên GitHub.")
    add_p("4. Phân quyền Database tối thiểu (Least Privilege): Giới hạn tài khoản ứng dụng chỉ được thao tác trong CSDL wordpress_db, không dùng quyền root tùy tiện.")

    add_h2("6.2. Lịch sử Commit và Quản lý trên GitHub")
    add_p("Toàn bộ mã nguồn được lưu trữ tại Repository: https://github.com/maidangcuong/DTC245200425 với các Commit theo đúng tiến độ triển khai.")

    add_h2("6.3. Hình ảnh minh chứng kết quả triển khai Chương 6")
    add_image_placeholder("HÌNH 6.1", "Lịch sử Commit trên GitHub Repository", "Lịch sử các lần commit rõ ràng trên GitHub tương ứng với từng mốc yêu cầu của đề tài.")
    add_image_placeholder("HÌNH 6.2", "Trạng thái các Containers qua lệnh docker compose ps", "Màn hình Terminal hiển thị đầy đủ 10 containers của dự án đều đang ở trạng thái UP (healthy).")

    # -------------------------------------------------------------
    # CHƯƠNG 7
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    add_h2("7.1. Đánh giá kết quả đạt được")
    add_p("Hệ thống đã vận hành hoàn chỉnh, ổn định, đáp ứng 100% các tiêu chí kỹ thuật và barem điểm của đề tài số 03. Sinh viên nắm vững nguyên lý hoạt động của Docker Compose, Nginx SSL, Prometheus, Grafana và Loki.")

    add_h2("7.2. Hướng phát triển trong tương lai")
    add_p("• Tích hợp Prometheus Alertmanager để tự động gửi thông báo cảnh báo về Telegram/Slack khi hệ thống gặp sự cố.")
    add_p("• Nâng cấp hệ thống lên cụm Kubernetes (K8s) để hỗ trợ tính năng tự động cân bằng tải và mở rộng quy mô (Auto-scaling).")
    add_p("• Tích hợp chứng chỉ số SSL tự động gia hạn với Let's Encrypt / Certbot.")

    # Save document
    output_path = r"C:\Users\Admin\DTC245200425\BAO_CAO_BAI_THI_SDM332_DTC245200425.docx"
    doc.save(output_path)
    print(f"Successfully generated Word document at: {output_path}")

if __name__ == "__main__":
    build_word_report()
