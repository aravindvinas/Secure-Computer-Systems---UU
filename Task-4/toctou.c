/*
 * file: toctou.c
 * desc: This program attempts to exploit the TOCTOU vulnerabilities in the POSIX stack
 * author : ap
 */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    const char *filename = "testfile.txt";
    
    /*
     * 1. Open the file for writing (Check & Open phase)
     * O_WRONLY: open for writing
     * O_CREAT: create if missing
     * O_TRUNC: truncate to 0 bytes
     * Mode 0644: owner read/write, group/others read-only
     */
    
    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("[-] Error opening file (Check failed)");
        exit(EXIT_FAILURE);
    }
    printf("File '%s' opened successfully. File Descriptor: %d\n", filename, fd);

    /* 2. Stop and wait for input from the user (The TOCTTOU vulnerability window) */
    printf("Program paused. Modify permissions or delete the file now, then press ENTER to write...\n");
    getchar();

    /* 3. Write on the file descriptor (Use phase) */
    const char *data = "TOCTTOU Demonstration\n";
    ssize_t bytes_written = write(fd, data, 49);
    if (bytes_written < 0) {
        perror("Error writing to file descriptor (Use failed)");
    } else {
        printf("Successfully wrote %zd bytes to file descriptor %d.\n", bytes_written, fd);
    }

    /* 4. Close the file descriptor */
    if (close(fd) < 0) {
        perror("Error closing file descriptor");
    } else {
        printf("File descriptor closed successfully.\n");
    }

    return 0;
}