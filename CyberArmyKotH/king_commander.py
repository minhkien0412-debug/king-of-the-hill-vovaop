"""
==============================================================================
KING COMMANDER - BỘ NÃO ĐIỀU PHỐI TRUNG TÂM (PYTHON 3.14+)
==============================================================================
Module chính điều phối toàn bộ hệ thống CyberArmy KotH Edition V10.8.
Kết hợp sức mạnh của đa ngôn ngữ (Python, C, Bash) trong một kiến trúc 
bất đồng bộ (asyncio) hiện đại và an toàn.

Chức năng chính:
- Army Deployment: Kích hoạt các module con (C Monitor, Bash Maintainer, Decoy).
- Flag Discovery: Tự động tìm kiếm đường dẫn flag thật khi khởi động.
- Safe Cleanup: Dọn dẹp tài nguyên và dừng tiến trình con an toàn khi thoát.
- Heartbeat Loop: Duy trì vòng lặp ghi flag dự phòng ở mức độ ưu tiên thấp.
"""

import asyncio
import time
import os
import sys
import signal
import subprocess
from typing import Any, Optional

# Import các module chiến thuật từ package units
from units.decoy_engine import DecoyEngine
from units.flag_hunter import CyberArmyFlagHunter

class CyberArmyPureCommander:
    """
    [The Pure Python 3.14 Brain Commander - Spec 2026]
    Bộ não Thủ lĩnh thuần túy. Chỉ lo khâu tư duy giải thuật logic.
    Điều hành trận chiến bằng cách quản lý và phát lệnh gọi các toán quân 
    C và Bash độc lập chạy song song.
    """
    
    def __init__(self):
        """Khởi tạo bộ chỉ huy với các tham số mặc định."""
        self.team_id: str = "CyberArmy_V10_8"
        self.flag_path: str = "/var/www/html/flag.txt"  # Đường dẫn mặc định
        self.is_battle_active: bool = True
        
        # Khởi tạo các thành phần chiến thuật
        self.decoy_engine: DecoyEngine = DecoyEngine()
        self.flag_hunter: CyberArmyFlagHunter = CyberArmyFlagHunter()
        
        # Danh sách các tiến trình con được quản lý
        self.child_processes: list[subprocess.Popen] = []
        
        # Thiết lập các hàm thu dọn tài nguyên hệ thống an toàn khi dừng chương trình
        signal.signal(signal.SIGTERM, self.safe_cleanup_handler)
        signal.signal(signal.SIGINT, self.safe_cleanup_handler)

    def deploy_army_modules(self) -> None:
        """
        Phóng thích các toán quân đa ngôn ngữ độc lập ra thao trường.
        Mỗi module chạy song song như một tiến trình riêng biệt.
        """
        print("[🧠 BRAIN] Phát lệnh kích nổ bầy quân đa ngôn ngữ độc lập thực chiến...")
        
        # 1. Kích hoạt File chạy nhị phân C (Bộ giám sát tiến trình an toàn)
        # Lưu ý: File này cần được biên dịch trước bằng lệnh: 
        # gcc modules/process_monitor.c -o modules/process_monitor
        try:
            c_process = subprocess.Popen(
                ["./modules/process_monitor"], 
                stderr=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                text=True
            )
            self.child_processes.append(c_process)
            print("[+] [C23] Process Monitor started (PID: {}).".format(c_process.pid))
        except FileNotFoundError:
            print("[-] [C23] Lỗi: Không tìm thấy file nhị phân 'process_monitor'. Vui lòng biên dịch trước.")
        except Exception as e:
            print(f"[-] [C23] Failed to start Process Monitor: {e}")
        
        # 2. Kích hoạt toán quân Bash duy trì nộp flag liên tục
        try:
            bash_process = subprocess.Popen(
                ["bash", "modules/flag_maintainer.sh"], 
                stderr=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                text=True
            )
            self.child_processes.append(bash_process)
            print("[+] [Bash] Flag Maintainer started (PID: {}).".format(bash_process.pid))
        except Exception as e:
            print(f"[-] [Bash] Failed to start Flag Maintainer: {e}")

        # 3. Kích hoạt chiến thuật tấn công giả (Decoy Engine)
        # Chạy trong luồng nền của Python, không cần subprocess
        self.decoy_engine.start_distraction()

    def safe_cleanup_handler(self, signum: int, frame: Any) -> None:
        """
        [CLEANUP HOOK] Thu hồi luồng RAM và dừng quân đội an toàn.
        Đảm bảo không để lại tiến trình rác hay file tạm khi thoát.
        """
        print("\n[+] [Cleanup] Bộ não phát lệnh rút quân. Tiến hành dọn dẹp hệ thống...")
        self.is_battle_active = False
        
        # 1. Dừng Decoy Engine (Xóa file giả)
        try:
            self.decoy_engine.stop_distraction()
        except Exception:
            pass
        
        # 2. Dập tắt các tiến trình con (C và Bash) một cách êm ái
        for proc in self.child_processes:
            try:
                if proc.poll() is None:  # Nếu tiến trình vẫn đang chạy
                    proc.terminate()     # Gửi SIGTERM trước
                    try:
                        proc.wait(timeout=3)  # Chờ tối đa 3s
                    except subprocess.TimeoutExpired:
                        proc.kill()           # Nếu cứng đầu thì dùng SIGKILL
            except Exception:
                pass
        
        # 3. Dự phòng: Dùng pkill để chắc chắn không còn tiến trình nào sót lại
        subprocess.run("pkill -f process_monitor", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("pkill -f flag_maintainer.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("[+] [Cleanup] Hoàn tất. Hệ thống đã trở về trạng thái an toàn.")
        sys.exit(0)

    async def main_battle_loop(self) -> None:
        """
        Vòng lặp chiến đấu chính (Main Event Loop).
        Chạy bất đồng bộ để không chặn các tác vụ khác.
        """
        print("================================================================")
        print(f"[+] CYBERARMY POLYGLOT PURE BRAIN STARTED CHÍNH THỨC (SPEC-2026)")
        print(f"[i] Team ID: {self.team_id}")
        print("================================================================")
        
        # Giai đoạn 1: Trinh sát tìm flag thật
        print("\n[🔍 SCOUT] Đang quét hệ thống để tìm flag thật...")
        real_flag = self.flag_hunter.fast_surface_scan()
        if real_flag:
            self.flag_path = real_flag
            print(f"[+] Tìm thấy flag thật tại: {self.flag_path}")
        else:
            print(f"[-] Chưa tìm thấy flag thật, sử dụng đường dẫn mặc định: {self.flag_path}")

        # Giai đoạn 2: Phóng thích quân đội
        print("\n[🚀 DEPLOY] Triển khai lực lượng chiến đấu...")
        self.deploy_army_modules()
        
        print("\n[⚔️ BATTLE] Hệ thống đang hoạt động. Nhấn Ctrl+C để dừng.")
        
        # Giai đoạn 3: Vòng lặp duy trì nhịp tim (Heartbeat)
        # Ghi flag dự phòng mỗi 5 giây nếu script Bash gặp sự cố
        while self.is_battle_active:
            try:
                # Chỉ thực hiện nếu có quyền root hoặc quyền ghi
                if os.getuid() == 0 or os.access(self.flag_path, os.W_OK):
                    with open(self.flag_path, "w") as f: 
                        f.write(f"{self.team_id}\n")
                
                # Ngủ 5 giây giữa các lần ghi (nhịp độ an toàn)
                await asyncio.sleep(5.0)
                
            except PermissionError:
                # Im lặng bỏ qua nếu không có quyền ghi (đã có Bash lo)
                await asyncio.sleep(5.0)
            except Exception as e:
                # Log lỗi nghiêm trọng nếu có
                # print(f"[Error] Heartbeat failed: {e}")
                await asyncio.sleep(5.0)

if __name__ == "__main__":
    # Kiểm tra quyền root khuyến nghị
    if os.getuid() != 0:
        print("[!] Cảnh báo: Nên chạy chương trình với quyền root (sudo) để đảm bảo hiệu năng tối đa.")
        # Không bắt buộc dừng, nhưng có thể một số tính năng sẽ bị hạn chế

    commander = CyberArmyPureCommander()
    try:
        # Chạy vòng lặp bất đồng bộ chính
        asyncio.run(commander.main_battle_loop())
    except KeyboardInterrupt:
        # Xử lý ngắt từ bàn phím (Ctrl+C)
        commander.is_battle_active = False
        # Handler signal sẽ lo phần dọn dẹp
        sys.exit(0)
    except Exception as e:
        print(f"[FATAL] Lỗi không mong muốn: {e}")
        sys.exit(1)
