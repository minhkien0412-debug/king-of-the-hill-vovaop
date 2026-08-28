#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>

int is_numerical_dir(const char *name) {
    for (size_t i = 0; name[i] != '\0'; ++i) {
        if (name[i] < '0' || name[i] > '9') return 0;
    }
    return 1;
}

void run_process_monitor(void) {
    printf("[+] [C23 Monitor] Khởi động Bộ giám sát tiến trình an toàn...\n");
    
    while (1) {
        DIR *dir = opendir("/proc");
        if (!dir) {
            sleep(1);
            continue;
        }

        struct dirent *entry;
        while ((entry = readdir(dir)) != NULL) {
            if (entry->d_type == DT_DIR && is_numerical_dir(entry->d_name)) {
                int pid = atoi(entry->d_name);
                if (pid == getpid() || pid == getppid()) continue;

                char cmd_path[256];
                snprintf(cmd_path, sizeof(cmd_path), "/proc/%d/cmdline", pid);
                
                FILE *f = fopen(cmd_path, "r");
                if (f) {
                    char cmdline[1024] = {0};
                    if (fgets(cmdline, sizeof(cmdline), f)) {
                        if (strstr(cmdline, "nc") || strstr(cmdline, "netcat") || 
                            strstr(cmdline, "socat") || strstr(cmdline, "webshell")) {
                            printf("[⚠️ ALERT] Phát hiện tiến trình khả nghi PID %d: %s\n", pid, cmdline);
                        }
                    }
                    fclose(f);
                }
            }
        }
        closedir(dir);
        sleep(1);
    }
}

int main(void) {
    run_process_monitor();
    return 0;
}
