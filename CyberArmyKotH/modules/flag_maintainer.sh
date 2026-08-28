#!/bin/bash
# ==============================================================================
# CYBERARMY V10.8 - SAFE FLAG MAINTAINER (BASH 5.3+ OPTIMIZED)
# ==============================================================================
# Module duy trì flag an toàn, tuân thủ luật thi đấu (SLA Compliant).
# 
# Giải thuật hoạt động:
# - Periodic Write: Ghi tên đội vào file flag với chu kỳ an toàn (5 giây).
# - No Subshell: Sử dụng builtin commands để tối ưu hiệu năng.
# - Safe I/O: Tránh gây bão đĩa cứng, đảm bảo ổn định hệ thống.
#
# Lưu ý: Không sử dụng 'chattr' hay khóa file. Chỉ ghi đè văn bản thông thường.

# Cấu hình tham số
FLAG_PATH="/var/www/html/flag.txt"
TEAM_ID="CyberArmy_V10_8"

# Chu kỳ ghi an toàn: 5 giây
# Đủ nhanh để giữ điểm trong hầu hết hệ thống chấm điểm KotH
# Đủ chậm để không bị coi là tấn công DoS I/O
SLEEP_INTERVAL=5

echo "[+] [Bash Maintainer] Bắt đầu duy trì flag với chu kỳ ${SLEEP_INTERVAL}s..."
echo "[i] Đường dẫn flag: ${FLAG_PATH}"
echo "[i] Tên đội: ${TEAM_ID}"

# Vòng lặp chính
while true; do
    # Kiểm tra quyền ghi trước khi thực hiện
    if [ -w "$FLAG_PATH" ]; then
        # Sử dụng printf để ghi an toàn và nhanh chóng
        printf "%s\n" "$TEAM_ID" > "$FLAG_PATH" 2>/dev/null
        echo "[$(date +%H:%M:%S)] Đã cập nhật flag."
    else
        # Cảnh báo nếu không có quyền ghi (có thể do file bị xóa hoặc đổi quyền)
        echo "[$(date +%H:%M:%S)] [!] Cảnh báo: Không thể ghi vào ${FLAG_PATH}. Kiểm tra quyền truy cập."
    fi
    
    # Ngủ đúng chu kỳ đã định
    sleep "$SLEEP_INTERVAL"
done
