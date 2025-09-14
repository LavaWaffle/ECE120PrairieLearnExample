#include <stdio.h>

int main() {
    int result = 0;
    int power = 1 << 5;

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