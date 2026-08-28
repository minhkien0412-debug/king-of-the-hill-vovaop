# ==============================================================================
# MODULES PACKAGE INITIALIZER
# ==============================================================================
# Khởi tạo package chứa các module thực thi độc lập đa ngôn ngữ (C, Bash).
# Các module này chạy song song dưới sự điều phối của King Commander.

__all__ = [
    # Lưu ý: process_monitor.c và flag_maintainer.sh là file nhị phân/script, 
    # không thể import trực tiếp vào Python mà được gọi qua subprocess.
]
