"""
==============================================================================
TARGET REQUEST GATE - CỔNG ĐIỀU PHỐI MẠNG (PYTHON 3.14+)
==============================================================================
Module này triển khai thuật toán Token Bucket kết hợp Sliding Window Latency 
để kiểm soát tốc độ gửi request, bảo vệ băng thông mạng và tránh bị coi là DDoS.

Thuật toán:
- Token Bucket: Hồi phục token tuyến tính theo thời gian thực.
- Sliding Window: Lưu 50 mẫu latency gần nhất để tính độ trễ trung bình.
- Adaptive Sleeping: Tự động điều chỉnh thời gian chờ dựa trên độ trễ mạng.
"""

import asyncio
import time
from typing import Callable, Any, List

class TargetRequestGate:
    """
    Cổng kiểm soát lưu lượng truy cập mạng thông minh.
    Đảm bảo tuân thủ SLA bằng cách giới hạn số request/giây.
    """
    
    def __init__(self, requests_per_sec: int = 30):
        """
        Khởi tạo cổng với hạn mức request mỗi giây.
        
        Args:
            requests_per_sec: Số lượng request tối đa được phép gửi mỗi giây.
        """
        self.capacity: int = requests_per_sec
        self.tokens: float = float(requests_per_sec)
        self.last_update: float = time.time()
        self.lock: asyncio.Lock = asyncio.Lock()
        self.latency_window: List[float] = []
        self.window_size: int = 50  # Kích thước cửa sổ trượt

    async def consume_token(self) -> bool:
        """
        Tiêu thụ một token nếu có sẵn. Cập nhật số lượng token dựa trên thời gian trôi qua.
        
        Returns:
            True nếu tiêu thụ thành công, False nếu hết token.
        """
        async with self.lock:
            now: float = time.time()
            elapsed: float = now - self.last_update
            
            # Hồi phục token tuyến tính theo thời gian
            self.tokens = min(float(self.capacity), self.tokens + (elapsed * self.capacity))
            self.last_update = now
            
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

    async def execute(self, task_id: str, async_coro: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Thực thi một coroutine bất đồng bộ sau khi đã kiểm tra token.
        Đo lường latency và cập nhật cửa sổ trượt.
        
        Args:
            task_id: Định danh duy nhất cho tác vụ (dùng cho logging/debug).
            async_coro: Coroutine cần thực thi.
            *args, **kwargs: Tham số truyền vào coroutine.
            
        Returns:
            Kết quả của coroutine hoặc None nếu có lỗi.
        """
        # Chờ đến khi có token
        while not await self.consume_token():
            await asyncio.sleep(0.005)  # Sleep ngắn để tránh busy-waiting
            
        start: float = time.time()
        try:
            result = await async_coro(*args, **kwargs)
            latency = time.time() - start
            
            # Cập nhật cửa sổ trượt latency
            self.latency_window.append(latency)
            if len(self.latency_window) > self.window_size: 
                self.latency_window.pop(0)
                
            return result
        except Exception as e:
            # Log lỗi nếu cần, ở đây trả về None để không làm gián đoạn luồng chính
            # print(f"[Error] Task {task_id} failed: {e}")
            return None

    def get_adaptive_delay(self) -> float:
        """
        Tính toán độ trễ thích ứng dựa trên trung bình cộng của cửa sổ trượt latency.
        
        Returns:
            Độ trễ trung bình (giây), hoặc giá trị mặc định 0.02s nếu chưa có dữ liệu.
        """
        if not self.latency_window:
            return 0.02
        return sum(self.latency_window) / len(self.latency_window)

    def get_current_load(self) -> float:
        """
        Trả về tỷ lệ tải hiện tại của cổng (0.0 đến 1.0).
        
        Returns:
            Tỷ lệ token đã sử dụng.
        """
        return 1.0 - (self.tokens / self.capacity)
