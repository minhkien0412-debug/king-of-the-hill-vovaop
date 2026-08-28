#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <time.h>

/**
 * ==============================================================================
 * PROCESS MONITOR - GIÁM SÁT TIẾN TRÌNH AN TOÀN (C23 STANDARD)
 * ==============================================================================
 * Module này duyệt thư mục /proc để phát hiện các tiến trình khả nghi 
 * (backdoor, reverse shell) nhưng CHỈ CẢNH BÁO, không thực hiện hành động kill.
 * 
 * Thuật toán:
 * - Linear Proc Scanning: Duyệt tuần tự các PID trong /proc.
 * - Pattern Matching: Tìm kiếm chuỗi nguy hiểm trong cmdline.
 * - Safe Reporting: In cảnh báo ra stdout thay vì can thiệp hệ thống.
 * 
 * Lưu ý: Để tuân thủ luật thi đấu (SLA Compliant), module này không gửi tín hiệu SIGKILL.
 */

// Hàm kiểm tra tên thư mục có phải là số (PID) không
// Trả về 1 nếu là số, 0 nếu không phải
static int is_numerical_dir(const char *name) {
    if (name == NULL || *name == '\0') return 0;
    
    for (size_t i = 0; name[i] != '\0'; ++i) {
        if (name[i] < '0' || name[i] > '9') return 0;
    }
    return 1;
}

// Hàm in timestamp hiện tại để log cho đẹp
static void print_timestamp(void) {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    printf("[%02d:%02d:%02d] ", t->tm_hour, t->tm_min, t->tm_sec);
}

void run_process_monitor(void) {
    printf("[+] [C23 Monitor] Khởi động Bộ giám sát tiến trình an toàn...\n");
    printf("[!] Chế độ chỉ cảnh báo (Safe Mode): Không thực hiện kill tiến trình.\n\n");
    
    // Vòng lặp vô tận với nhịp quét an toàn
    while (1) {
        DIR *dir = opendir("/proc");
        if (!dir) {
            // Nếu không mở được /proc, ngủ 1 giây rồi thử lại
            sleep(1);
            continue;
        }

        struct dirent *entry;
        while ((entry = readdir(dir)) != NULL) {
            // Chỉ xử lý các thư mục có tên là số (PID)
            if (entry->d_type == DT_DIR && is_numerical_dir(entry->d_name)) {
                int pid = atoi(entry->d_name);
                
                // Bỏ qua tiến trình hiện tại và tiến trình cha để tránh self-interference
                if (pid == getpid() || pid == getppid()) continue;

                char cmd_path[256];
                snprintf(cmd_path, sizeof(cmd_path), "/proc/%d/cmdline", pid);
                
                FILE *f = fopen(cmd_path, "r");
                if (f) {
                    char cmdline[1024] = {0};
                    // Đọc dòng lệnh khởi tạo tiến trình
                    if (fgets(cmdline, sizeof(cmdline), f)) {
                        // Danh sách các từ khóa nguy hiểm cần giám sát
                        // Nếu phát hiện, IN CẢNH BÁO ra màn hình
                        if (strstr(cmdline, "nc") || strstr(cmdline, "netcat") || 
                            strstr(cmdline, "socat") || strstr(cmdline, "webshell") ||
                            strstr(cmdline, "bash -i") || strstr(cmdline, "/bin/sh")) {
                            
                            print_timestamp();
                            printf("[⚠️ ALERT] Phát hiện tiến trình khả nghi PID %d: %s\n", pid, cmdline);
                            fflush(stdout); // Đảm bảo output được in ngay lập tức
                        }
                    }
                    fclose(f);
                }
            }
        }
        closedir(dir);
        
        // Nhịp quét: 1 giây/lần (Đủ nhanh để phát hiện, đủ chậm để không gây tải CPU)
        sleep(1);
    }
}

int main(void) {
    // Buffer stdout để in log mượt mà hơn
    setbuf(stdout, NULL);
    run_process_monitor();
    return 0;
}
