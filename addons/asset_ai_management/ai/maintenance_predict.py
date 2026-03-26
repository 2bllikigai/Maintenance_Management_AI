from datetime import date, timedelta
import numpy as np
import logging

_logger = logging.getLogger(__name__)

try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def predict_next_maintenance(asset, maintenance_records):
    """
    AI dự đoán ngày bảo trì tiếp theo dựa trên:
    1. Tỷ lệ khấu hao (Tài chính)
    2. Chi phí bảo trì lần cuối (Tài chính)
    3. Tốc độ hao mòn thực tế (Kỹ thuật) - MỚI CẬP NHẬT
    """
    
    # 1. Kiểm tra dữ liệu gốc
    if not asset.original_value or asset.original_value <= 0:
        return date.today() + timedelta(days=30)

    # Tính tỷ lệ khấu hao tổng thể
    current = asset.current_value or asset.original_value
    depreciation_rate = (asset.original_value - current) / asset.original_value

    # =====================
    # PHẦN 1: MACHINE LEARNING (Linear Regression)
    # =====================
    if SKLEARN_AVAILABLE and len(maintenance_records) >= 3:
        try:
            # Sắp xếp lịch sử bảo trì theo thời gian
            records = sorted(maintenance_records, key=lambda x: x.maintenance_date)
            
            X = [] # Tính năng: [Khấu hao, Chi phí, Tốc độ hao mòn]
            y = [] # Mục tiêu: Số ngày giãn cách giữa các lần bảo trì

            for i in range(1, len(records)):
                d1 = records[i-1].maintenance_date
                d2 = records[i].maintenance_date
                
                if d1 and d2:
                    interval = (d2 - d1).days
                    if interval > 0:
                        # Tính Wear Rate: Mức độ hao mòn tăng lên bao nhiêu mỗi ngày
                        deg_diff = records[i].degradation_level - records[i-1].degradation_level
                        wear_rate = deg_diff / interval if deg_diff > 0 else 0
                        
                        X.append([float(depreciation_rate), float(records[i].cost), float(wear_rate)])
                        y.append(interval)

            if len(X) >= 2:
                model = LinearRegression()
                model.fit(X, y)
                
                # Dự đoán cho lần tiếp theo
                last_record = records[-1]
                # Giả định Wear Rate lần tới tương đương lần gần nhất
                last_interval = (records[-1].maintenance_date - records[-2].maintenance_date).days if len(records) >= 2 else 30
                last_wear_rate = (records[-1].degradation_level - records[-2].degradation_level) / last_interval if last_interval > 0 else 0
                
                prediction_input = [[float(depreciation_rate), float(last_record.cost), float(last_wear_rate)]]
                predicted_days = model.predict(prediction_input)[0]
                
                # Giới hạn an toàn (3 - 90 ngày)
                predicted_days = int(max(3, min(predicted_days, 90)))
                return date.today() + timedelta(days=predicted_days)
        except Exception as e:
            _logger.error("Lỗi khi chạy AI Linear Regression: %s", str(e))

    # =====================
    # PHẦN 2: FALLBACK (RULE-BASED) - Dùng khi thiếu dữ liệu ML
    # =====================
    # Lấy mặc định từ Danh mục (nếu có cấu hình) hoặc dùng logic khấu hao
    default_days = 30
    if asset.category_id and asset.category_id.method_number > 0:
        # Nếu máy có vòng đời ngắn (khấu hao nhanh), tần suất bảo trì phải cao hơn
        default_days = max(15, int(asset.category_id.method_number / 2))

    if depreciation_rate > 0.7:
        days = 7   # Máy quá cũ (70% khấu hao) -> 1 tuần
    elif depreciation_rate > 0.4:
        days = 15  # Máy trung bình -> 2 tuần
    else:
        days = default_days # Máy mới -> Theo danh mục

    # Hiệu chỉnh theo tình trạng hiện tại
    if asset.condition == 'good':
        days += 5
    elif asset.condition == 'bad':
        days -= 5

    return date.today() + timedelta(days=max(3, days))  