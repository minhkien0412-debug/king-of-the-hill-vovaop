"""
==============================================================================
DECOY ENGINE - CHIẾN THUẬT TẤN CÔNG GIẢ (PYTHON 3.14+)
==============================================================================
Module này tạo ra các "mồi nhử" (decoys) để đánh lạc hướng đối thủ và làm nhiễu
hệ thống giám sát của đối phương, giúp che giấu hoạt động thật của quân chủ lực.

Thuật toán:
- Dynamic Decoy Generation: Sinh ngẫu nhiên các file flag giả có cấu trúc giống thật.
- Log Noise Injection: Tạo các timestamp truy cập giả để làm nhiễu log hệ thống.
- Self-Cleanup: Tự động dọn dẹp dấu vết khi kết thúc chiến dịch để tránh rác hệ thống.
"""

import os
import random
import string
import time
import threading
from typing import List

class DecoyEngine:
    """
    Bộ chỉ huy chiến thuật Ma Ảo (Ghost Tactics).
    Tạo ra hàng loạt mục tiêu giả để tiêu hao tài nguyên phân tích của đối thủ.
    """
    
    def __init__(self, base_path: str = "/tmp/.decoy_cyberarmy"):
        """
        Khởi tạo engine với thư mục chứa decoy.
        
        Args:
            base_path: Đường dẫn thư mục gốc để chứa các file giả mạo.
        """
        self.base_path: str = base_path
        self.is_running: bool = False
        self.decoy_files: List[str] = []
        self.max_decoys: int = 15  # Giới hạn số lượng file giả tối đa để tránh đầy đĩa
        
        # Danh sách các mẫu flag giả trông rất thật
        self.fake_flags: List[str] = [
            "FLAG{fake_decoy_001}",
            "KOTH{illusion_trap}",
            "FLAG{not_real_flag}",
            "CTF{honeypot_active}",
            "FLAG{wrong_path_here}",
            "KOTH{you_got_tricked}",
            "FLAG{decoy_generator_v1}",
            "CTF{this_is_bait}"
        ]
        
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(self.base_path):
            try:
                os.makedirs(self.base_path, exist_ok=True)
                # Đặt quyền truy cập hạn chế cho thư mục decoy
                os.chmod(self.base_path, 0o700)
            except Exception:
                pass

    def start_distraction(self) -> None:
        """Kích hoạt luồng chạy nền để sinh decoy liên tục."""
        if self.is_running:
            return
            
        self.is_running = True
        thread = threading.Thread(target=self._run_decoy_loop, daemon=True)
        thread.start()
        print("[👻 DECOY] Chiến thuật Ma Ảo đã kích hoạt...")

    def stop_distraction(self) -> None:
        """Dừng việc sinh decoy và dọn dẹp toàn bộ dấu vết."""
        self.is_running = False
        self._cleanup_decoys()
        print("[👻 DECOY] Đã dừng chiến thuật Ma Ảo và dọn dẹp hiện trường.")

    def _generate_random_content(self, length: int = 64) -> str:
        """Sinh chuỗi ký tự ngẫu nhiên để làm nội dung phụ cho file giả."""
        return ''.join(random.choices(string.ascii_letters + string.digits + "_-#", k=length))

    def _create_fake_flag(self) -> str:
        """
        Tạo một file flag giả hoàn chỉnh.
        
        Returns:
            Đường dẫn đến file vừa tạo.
        """
        # Tên file ngẫu nhiên giống như file system thông thường
        filename = f".flag_{random.randint(1000, 9999)}.txt"
        filepath = os.path.join(self.base_path, filename)
        
        # Nội dung: 1 dòng flag giả + dữ liệu rác để tăng độ tin cậy
        content = f"{random.choice(self.fake_flags)}\n# Generated: {time.time()}\n{self._generate_random_content()}"
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            
            # Giả lập thời gian sửa đổi ngẫu nhiên trong quá khứ gần để tránh bị phát hiện
            random_time_offset = random.uniform(60, 3600)  # 1 phút đến 1 giờ trước
            os.utime(filepath, (time.time() - random_time_offset, time.time() - random_time_offset))
            
            self.decoy_files.append(filepath)
            return filepath
        except Exception:
            return ""

    def _run_decoy_loop(self) -> None:
        """Vòng lặp chính sinh và duy trì decoy."""
        while self.is_running:
            try:
                # Sinh một file giả mới
                fake_path = self._create_fake_flag()
                
                if fake_path:
                    # Cập nhật thời gian truy cập để làm nhiễu log monitoring
                    os.utime(fake_path, None) 
                
                # Ngủ ngẫu nhiên để tạo pattern không đều, khó bị phát hiện bởi heuristic
                time.sleep(random.uniform(2.0, 6.0))
                
                # Quản lý bộ nhớ: Xóa file cũ nếu vượt quá giới hạn
                if len(self.decoy_files) > self.max_decoys:
                    old_file = self.decoy_files.pop(0)
                    if os.path.exists(old_file):
                        try:
                            os.remove(old_file)
                        except Exception:
                            pass
                            
            except Exception:
                # Lỗi không quan trọng, tiếp tục vòng lặp
                time.sleep(1.0)

    def _cleanup_decoys(self) -> None:
        """Xóa toàn bộ file decoy đã tạo để dọn dẹp hiện trường."""
        for f in self.decoy_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        
        # Cố gắng xóa thư mục gốc nếu rỗng
        try:
            if os.path.exists(self.base_path) and not os.listdir(self.base_path):
                os.rmdir(self.base_path)
        except Exception:
            pass
            
        self.decoy_files.clear()
