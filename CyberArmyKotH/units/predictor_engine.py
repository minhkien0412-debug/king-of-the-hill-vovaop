"""
==============================================================================
PREDICTOR ENGINE - BỘ DỰ ĐOÁN CHU KỲ CHẤM ĐIỂM (PYTHON 3.14+)
==============================================================================
Module này sử dụng thuật toán thống kê Median trên cửa sổ trượt (Sliding Window)
để dự đoán chính xác thời điểm Ban tổ chức cập nhật bảng xếp hạng (Tick).

Thuật toán:
- Sliding Window Time Differences: Lưu trữ 10 mốc thời gian gần nhất.
- Median of Differences: Tính trung vị của sai phân thời gian để loại bỏ nhiễu (outliers).
- Burst Activation: Gợi ý thời điểm "nổ" flag tối ưu dựa trên độ trễ mạng.
"""

import numpy as np
import time
from typing import List

class KotHTickPredictor:
    """
    Bộ dự đoán chu kỳ chấm điểm thông minh, giúp tối ưu hóa thời điểm gửi flag.
    Sử dụng NumPy để tính toán nhanh và chính xác.
    """
    
    def __init__(self, window_size: int = 10):
        """
        Khởi tạo bộ dự đoán với kích thước cửa sổ trượt.
        
        Args:
            window_size: Số lượng mốc thời gian gần nhất để lưu trữ và phân tích.
        """
        self.window_size: int = window_size
        self.timestamps: List[float] = []
        self.estimated_period: float = 60.0  # Giá trị mặc định an toàn (60 giây)

    def register_tick(self) -> None:
        """
        Ghi nhận một mốc thời gian xảy ra tick (cập nhật điểm).
        Tự động cập nhật chu kỳ ước lượng dựa trên trung vị sai phân.
        """
        current_time = time.time()
        self.timestamps.append(current_time)
        
        # Duy trì kích thước cửa sổ trượt
        if len(self.timestamps) > self.window_size: 
            self.timestamps.pop(0)
            
        # Chỉ tính toán khi có đủ ít nhất 2 mẫu
        if len(self.timestamps) >= 2:
            diffs = np.diff(self.timestamps)
            if len(diffs) > 0:
                # Sử dụng Median để loại bỏ các giá trị ngoại lai (do lag mạng đột biến)
                self.estimated_period = float(np.median(diffs))

    def get_seconds_until_next_tick(self) -> float:
        """
        Ước lượng thời gian còn lại cho đến tick tiếp theo.
        
        Returns:
            Số giây còn lại (float). Trả về 5.0 nếu chưa có dữ liệu.
        """
        if not self.timestamps: 
            return 5.0
            
        # Tính thời gian đã trôi qua kể từ tick cuối cùng modulo chu kỳ ước lượng
        time_since_last = time.time() - self.timestamps[-1]
        remaining = self.estimated_period - (time_since_last % self.estimated_period)
        
        return max(0.0, remaining)  # Đảm bảo không trả về số âm

    def should_activate_burst(self, network_latency: float) -> bool:
        """
        Quyết định xem có nên kích hoạt chế độ "bắn nhanh" (burst) hay không.
        Chế độ burst được kích hoạt khi thời gian còn lại đến tick rất ngắn,
        tương đương với vài lần độ trễ mạng.
        
        Args:
            network_latency: Độ trễ mạng trung bình hiện tại (giây).
            
        Returns:
            True nếu nên kích hoạt burst, False nếu chưa cần thiết.
        """
        seconds_left = self.get_seconds_until_next_tick()
        # Ngưỡng kích hoạt: Khi thời gian còn lại <= 4 lần độ trễ mạng
        threshold = network_latency * 4
        return seconds_left <= threshold

    def get_estimated_period(self) -> float:
        """
        Trả về chu kỳ chấm điểm ước lượng hiện tại.
        
        Returns:
            Chu kỳ (giây).
        """
        return self.estimated_period

    def reset(self) -> None:
        """Đặt lại toàn bộ dữ liệu lịch sử."""
        self.timestamps.clear()
        self.estimated_period = 60.0
