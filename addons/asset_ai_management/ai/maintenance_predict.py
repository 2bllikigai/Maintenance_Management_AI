from datetime import date, timedelta
import numpy as np

# Cố gắng import sklearn, nếu không có thì dùng rule-based
try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def predict_next_maintenance(asset, maintenance_records):
    """
    AI dự đoán ngày bảo trì tiếp theo.
    """
    
    # 1. Kiểm tra dữ liệu đầu vào cơ bản
    if not asset.original_value or asset.original_value == 0:
        return date.today() + timedelta(days=30) # Trả về mặc định nếu thiếu giá trị gốc

    # Tính tỷ lệ khấu hao (Depreciation Rate)
    # Nếu current_value chưa có, coi như bằng original_value
    current = asset.current_value or asset.original_value
    depreciation_rate = (asset.original_value - current) / asset.original_value

    # =====================
    # ML PART (Linear Regression)
    # =====================
    # SỬA LỖI: Đổi m.date thành m.maintenance_date
    if SKLEARN_AVAILABLE and len(maintenance_records) >= 3:
        # Lấy danh sách ngày và chi phí từ lịch sử
        dates = sorted([m.maintenance_date for m in maintenance_records if m.maintenance_date])
        costs = [m.cost for m in maintenance_records]

        X = [] # Tính năng: [tỷ lệ khấu hao, chi phí lần cuối]
        y = [] # Mục tiêu: số ngày giãn cách giữa các lần bảo trì

        for i in range(1, len(dates)):
            interval = (dates[i] - dates[i-1]).days
            if interval > 0:
                X.append([float(depreciation_rate), float(costs[i])])
                y.append(interval)

        # Huấn luyện mô hình nhanh nếu có đủ dữ liệu mẫu
        if len(X) >= 2:
            try:
                model = LinearRegression()
                model.fit(X, y)
                
                # Dự đoán số ngày dựa trên tình trạng hiện tại
                last_cost = costs[-1] if costs else 0
                predicted_days = model.predict([[float(depreciation_rate), float(last_cost)]])[0]
                
                # Giới hạn kết quả trong khoảng hợp lý (từ 3 đến 90 ngày)
                predicted_days = int(max(3, min(predicted_days, 90)))
                return date.today() + timedelta(days=predicted_days)
            except:
                pass # Nếu lỗi khi fit model thì chuyển xuống fallback

    # =====================
    # FALLBACK (RULE BASED)
    # Dự đoán dựa trên kinh nghiệm nếu thiếu dữ liệu ML
    # =====================
    if depreciation_rate > 0.7:
        days = 7   # Máy quá cũ -> 1 tuần bảo trì 1 lần
    elif depreciation_rate > 0.4:
        days = 15  # Máy trung bình -> 2 tuần
    else:
        days = 30  # Máy mới -> 1 tháng

    # Cộng thêm 1 khoảng nhỏ nếu tình trạng (condition) là 'good'
    if asset.condition == 'good':
        days += 5

    return date.today() + timedelta(days=days)