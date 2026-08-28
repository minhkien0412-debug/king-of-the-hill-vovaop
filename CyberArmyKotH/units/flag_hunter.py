"""
==============================================================================
FLAG HUNTER - TRINH SÁT TÌM CỜ THUẬT TOÁN (PYTHON 3.14+)
==============================================================================
Module này kết hợp duyệt đồ thị hệ thống tệp tin với bộ lọc Regex thông minh
để xác định nhanh chóng đường dẫn chính xác của file flag.

Thuật toán:
- Restricted BFS/DFS: Chỉ quét các thư mục người dùng thường gặp, bỏ qua vùng hệ thống.
- Heuristic Filtering: Lọc dựa trên kích thước file (<1KB) và thời gian sửa đổi.
- Regex Validation: Xác thực nội dung dựa trên mẫu FLAG{...} hoặc KOTH{...}.
"""

import os
import re
import subprocess
from typing import List, Optional

class CyberArmyFlagHunter:
    """
    Chuyên gia trinh sát tìm kiếm file flag thật trên hệ thống Linux.
    Tối ưu hóa I/O bằng cách loại bỏ các thư mục không cần thiết.
    """
    
    def __init__(self):
        # Danh sách các thư mục có khả năng chứa flag cao nhất
        self.search_paths: List[str] = ["/var/www", "/home", "/root", "/opt", "/tmp", "/srv"]
        
        # Danh sách các thư mục hệ thống cần loại bỏ tuyệt đối để tránh treo máy
        self.exclude_zones: List[str] = ["/proc", "/sys", "/dev", "/lib", "/usr", "/bin", "/sbin", "/boot"]
        
        # Biểu thức chính quy nhận diện flag chuẩn CTF/KotH
        self.flag_regex: re.Pattern = re.compile(r"(FLAG\{[A-Za-z0-9_#\-]+\}|KOTH\{[A-Za-z0-9_#\-]+\}|CTF\{[A-Za-z0-9_#\-]+\})", re.IGNORECASE)
        
        self.real_flag_path: Optional[str] = None

    def fast_surface_scan(self) -> Optional[str]:
        """
        Thực hiện quét nhanh bề mặt hệ thống để tìm ứng viên flag.
        Sử dụng lệnh 'find' của Linux để tối ưu tốc độ.
        
        Returns:
            Đường dẫn file flag nếu tìm thấy, ngược lại là None.
        """
        # Xây dựng lệnh find an toàn: Giới hạn phạm vi tìm kiếm
        # Tìm các file có tên chứa 'flag' hoặc '.flag'
        cmd_parts = ["find"] + self.search_paths + ["-type", "f", r"\( -name '*flag*' -o -name '.flag*' \)"]
        cmd = " ".join(cmd_parts) + " 2>/dev/null"
        
        try:
            # Chạy lệnh với timeout chặt chẽ để tránh treo vô tận
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            
            if res.returncode == 0 and res.stdout:
                candidates = res.stdout.strip().split("\n")
                
                # Ưu tiên kiểm tra các file tìm thấy đầu tiên (thường là gần nhất)
                for path in candidates:
                    if not path:
                        continue
                    # Bỏ qua nếu nằm trong vùng cấm (kiểm tra kép)
                    if any(path.startswith(zone) for zone in self.exclude_zones):
                        continue
                        
                    if self.verify_flag_authenticity(path):
                        self.real_flag_path = path
                        return path
                        
        except subprocess.TimeoutExpired:
            print("[!] Cảnh báo: Quét flag hết thời gian cho phép.")
        except Exception as e:
            # Im lặng thất bại để không làm nhiễu log chính
            pass
            
        return None

    def verify_flag_authenticity(self, file_path: str) -> bool:
        """
        Xác thực xem một file có phải là flag thật hay không dựa trên heuristic.
        
        Args:
            file_path: Đường dẫn tuyệt đối đến file cần kiểm tra.
            
        Returns:
            True nếu là flag thật (hoặc ứng viên nặng ký), False nếu không.
        """
        try:
            # Kiểm tra sự tồn tại
            if not os.path.exists(file_path): 
                return False
            
            # Kiểm tra kích thước: Flag thường rất ngắn (< 1KB)
            # File lớn hơn thường là log, binary hoặc data rác
            if os.path.getsize(file_path) > 1024: 
                return False

            # Đọc nội dung file (bỏ qua lỗi encoding)
            with open(file_path, "r", errors="ignore") as f: 
                content = f.read().strip()
            
            # Tiêu chí 1: Khớp với mẫu Regex chuẩn
            if self.flag_regex.search(content): 
                return True
                
            # Tiêu chí 2: File vừa được sửa đổi trong vòng 5 giây gần đây
            # (Dành cho trường hợp flag động hoặc vừa được tạo bởi script đối thủ/BTC)
            mtime = os.path.getmtime(file_path)
            if (time.time() - mtime) < 5.0 and len(content) < 100:
                return True
                
        except (IOError, OSError, PermissionError):
            # Không có quyền đọc hoặc lỗi hệ thống
            pass
        except Exception:
            pass
            
        return False

    def get_flag_path(self) -> Optional[str]:
        """Trả lại đường dẫn flag đã tìm thấy (nếu có)."""
        return self.real_flag_path
