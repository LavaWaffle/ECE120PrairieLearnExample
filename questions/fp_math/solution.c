#include <stdio.h>

int main() {
    // Get N
    int N;
    scanf("%d", &N);

    int result = 0;
    for (int i = 0; N > 0; i++) {
            // N % 10 gives the last digit in base 2
            result += (N % 10) * (1 << i); // 1 << i is 2^i
            // N /= 10 removes the last digit
            N /= 10; 
        }
    printf("%d", result);

    return 0;
}