#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    pid_t pid = fork();

    if (pid == -1) {
        perror("fork failed");
        return EXIT_FAILURE;
    } else if (pid == 0) {
        printf("Hello from the child process!\n");    
        return EXIT_SUCCESS;
    } else {
        int status;
        waitpid(pid, &status, 0);
    }

    printf("Hello from the parent process!\n");


    return EXIT_SUCCESS;
}