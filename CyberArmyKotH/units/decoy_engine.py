import os
import random
import string
import time
import threading
from typing import List

class DecoyEngine:
    def __init__(self, base_path: str = "/tmp/.decoy_cyberarmy"):
        self.base_path = base_path
        self.is_running = False
        self.decoy_files: List[str] = []
        self.fake_flags = [
            "FLAG{fake_decoy_001}",
            "KOTH{illusion_trap}",
            "FLAG{not_real_flag}",
            "CTF{honeypot_active}",
            "FLAG{wrong_path_here}"
        ]
        
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    def start_distraction(self):
        self.is_running = True
        thread = threading.Thread(target=self._run_decoy_loop, daemon=True)
        thread.start()
        print("[👻 DECOY] Chiến thuật Ma Ảo đã kích hoạt...")

    def stop_distraction(self):
        self.is_running = False
        self._cleanup_decoys()
        print("[👻 DECOY] Đã dừng chiến thuật Ma Ảo.")

    def _generate_random_content(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def _create_fake_flag(self) -> str:
        filename = f".flag_{random.randint(1000, 9999)}.txt"
        filepath = os.path.join(self.base_path, filename)
        content = random.choice(self.fake_flags) + "\n" + self._generate_random_content()
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        self.decoy_files.append(filepath)
        return filepath

    def _run_decoy_loop(self):
        while self.is_running:
            try:
                fake_path = self._create_fake_flag()
                os.utime(fake_path, None) 
                time.sleep(random.uniform(2.0, 5.0))
                
                if len(self.decoy_files) > 10:
                    old_file = self.decoy_files.pop(0)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                        
            except Exception:
                pass

    def _cleanup_decoys(self):
        for f in self.decoy_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        self.decoy_files.clear()
