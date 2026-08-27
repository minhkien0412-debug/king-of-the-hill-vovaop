import asyncio
import time
import os
import sys
import signal
import subprocess
from typing import Any

# Import các module con
from units.decoy_engine import DecoyEngine
from units.flag_hunter import CyberArmyFlagHunter

class CyberArmyPureCommander:
    """
    [The Pure Python 3.14 Brain Commander - Spec 2026]
    Bộ não Thủ lĩnh thuần túy. Điều hành trận chiến bằng cách quản lý 
    các toán quân C và Bash độc lập cùng chiến thuật Decoy.
    """
    def __init__(self):
        self.team_id: str = "CyberArmy_V10_8"
        self.flag_path: str = "/var/www/html/flag.txt"
        self.is_battle_active: bool = True
        
        # Khởi tạo các thành phần
        self.decoy_engine = DecoyEngine()
        self.flag_hunter = CyberArmyFlagHunter()
        
        # Thiết lập các hàm thu dọn tài nguyên hệ thống an toàn
        signal.signal(signal.SIGTERM, self.safe_cleanup_handler)
        signal.signal(signal.SIGINT, self.safe_cleanup_handler)

    def deploy_army_modules(self) -> None:
        """Thủ lĩnh gọi kích hoạt các toán quân đa ngôn ngữ độc lập thực thi nhiệm vụ"""
        print("[🧠 BRAIN] Phát lệnh kích nổ bầy quân đa ngôn ngữ độc lập thực chiến...")
        
        # 1. Kích hoạt File chạy nhị phân C (Bộ giám sát tiến trình)
        # Lưu ý: Cần biên dịch trước: gcc modules/process_monitor.c -o modules/process_monitor
        try:
            subprocess.Popen(["./modules/process_monitor"], stderr=subprocess.DEVNULL)
            print("[+] [C23] Process Monitor started.")
        except Exception as e:
            print(f"[-] [C23] Failed to start Process Monitor: {e}")
        
        # 2. Kích hoạt toán quân Bash duy trì nộp flag liên tục
        try:
            subprocess.Popen(["bash", "modules/flag_maintainer.sh"], stderr=subprocess.DEVNULL)
            print("[+] [Bash] Flag Maintainer started.")
        except Exception as e:
            print(f"[-] [Bash] Failed to start Flag Maintainer: {e}")

        # 3. Kích hoạt chiến thuật tấn công giả (Decoy)
        self.decoy_engine.start_distraction()

    def safe_cleanup_handler(self, signum: int, frame: Any) -> None:
        """[CLEANUP HOOK] Thu hồi luồng RAM và dừng quân đội an toàn"""
        print("\n[+] [Cleanup] Bộ não phát lệnh rút quân. Tiến hành dọn dẹp hệ thống...")
        self.is_battle_active = False
        
        # Dừng Decoy Engine
        self.decoy_engine.stop_distraction()
        
        # Dập tắt các tiến trình con khi Bộ não chủ động tắt
        subprocess.run("pkill -f process_monitor", shell=True)
        subprocess.run("pkill -f flag_maintainer.sh", shell=True)
        sys.exit(0)

    async def main_battle_loop(self) -> None:
        print("================================================================")
        print(f"[+] CYBERARMY POLYGLOT PURE BRAIN STARTED CHÍNH THỨC (SPEC-2026)")
        print("================================================================")
        
        # Tìm flag thật trước khi bắt đầu
        real_flag = self.flag_hunter.fast_surface_scan()
        if real_flag:
            self.flag_path = real_flag
            print(f"[+] Tìm thấy flag thật tại: {self.flag_path}")
        else:
            print("[-] Chưa tìm thấy flag thật, sử dụng đường dẫn mặc định.")

        # Phóng thích quân đội ra thao trường bảo vệ hệ thống
        self.deploy_army_modules()
        
        while self.is_battle_active:
            # Luồng tư duy chính: Giám sát trạng thái và ghi flag dự phòng nếu cần
            if os.getuid() == 0:
                try:
                    # Ghi nhẹ nhàng mỗi 5 giây để dự phòng cho script bash
                    with open(self.flag_path, "w") as f: 
                        f.write(f"{self.team_id}\n")
                except Exception: 
                    pass
            await asyncio.sleep(5.0)

if __name__ == "__main__":
    commander = CyberArmyPureCommander()
    try:
        asyncio.run(commander.main_battle_loop())
    except KeyboardInterrupt:
        commander.is_battle_active = False
        sys.exit(0)
