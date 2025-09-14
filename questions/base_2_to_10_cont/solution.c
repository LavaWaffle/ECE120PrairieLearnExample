#include <stdio.h>

// Convert from base 2 to base 10
int main() {
    int L;
    char garbage;
    scanf("%d%c", &L, &garbage);

    int power = 1 << (L - 1);
    int result = 0;

    while (power > 0) {
        char nextBit;
        scanf("%c", &nextBit);

        // Your code here!
        if (nextBit == '1') {
            result += power; 
        }
        power = power >> 1;
    }

    printf("%d", result);

    // Keep this return 0;
    return 0;
}