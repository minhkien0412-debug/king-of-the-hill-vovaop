import os
import re
import subprocess

class CyberArmyFlagHunter:
    def __init__(self):
        # Chỉ quét các vùng an toàn và có khả năng chứa flag
        self.search_paths = ["/var/www", "/home", "/root", "/opt", "/tmp"]
        self.exclude_zones = ["/proc", "/sys", "/dev", "/lib", "/usr", "/bin", "/sbin"]
        self.flag_regex = re.compile(r"(FLAG\{[A-Za-z0-9_#-]+\}|KOTH\{[A-Za-z0-9_#-]+\})")
        self.real_flag_path = None

    def fast_surface_scan(self) -> str | None:
        # Xây dựng lệnh find an toàn, giới hạn độ sâu và loại trừ thư mục hệ thống
        cmd = "find " + " ".join(self.search_paths) + " -type f \\( -name '*flag*' -o -name '.flag*' \\) 2>/dev/null"
        
        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True, timeout=5)
            if res.returncode == 0 and res.stdout:
                for path in res.stdout.strip().split("\n"):
                    if path and self.verify_flag_authenticity(path):
                        self.real_flag_path = path
                        return path
        except Exception: 
            pass
        return None

    def verify_flag_authenticity(self, file_path: str) -> bool:
        if not os.path.exists(file_path): 
            return False
        
        # Kiểm tra kích thước hợp lý (không quá lớn)
        try:
            if os.path.getsize(file_path) > 1024: 
                return False
        except Exception:
            return False

        try:
            with open(file_path, "r", errors="ignore") as f: 
                content = f.read().strip()
            # Kiểm tra nội dung hoặc thời gian sửa đổi gần đây
            if self.flag_regex.search(content): 
                return True
        except Exception: 
            pass
        return False
