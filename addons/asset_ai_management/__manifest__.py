{
    'name': 'Asset AI Management - Nhóm 5',
    'version': '1.0',
    'category': 'Manufacturing/Maintenance',
    'summary': 'Quản lý tài sản kết hợp AI dự báo bảo trì, Khấu hao kế toán và Quản lý nhân sự',
    'description': """
        Đồ án thực tập doanh nghiệp:
        - Quản lý vòng đời tài sản.
        - Tự động tính toán khấu hao hàng tháng (Đề tài 5).
        - AI dự báo ngày bảo trì tiếp theo bằng Linear Regression.
        - Kết nối module Nhân sự để giao việc bảo trì.
        - Tự động hạch toán chi phí bảo trì vào sổ cái kế toán.
    """,
    'author': 'Kiều Quang Trường & Nhóm 5',
    'website': 'https://github.com/2bllikigai/Maintenance_Management_AI', # Link Github của Trường
    
    # Bắt buộc phải có 'mail' để dùng Chatter và Activity nhắc việc
    'depends': ['base', 'hr', 'account', 'mail'],

    'data': [
        # 1. Phân quyền phải nạp đầu tiên
        'security/ir.model.access.csv',
        
        # 2. Dữ liệu cấu hình (Sequence, Cron)
        'data/ir_sequence_data.xml',
        'data/cron.xml',
        
        # 3. Giao diện (Thứ tự: Danh mục -> Tài sản -> Bảo trì -> Yêu cầu)
        'views/asset_category_view.xml',
        'views/asset_views.xml',
        'views/maintenance_views.xml',
        'views/asset_request_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}