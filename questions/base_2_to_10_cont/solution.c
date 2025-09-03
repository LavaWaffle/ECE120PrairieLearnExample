#include <stdio.h>

// Convert from base 2 to base 10
int main() {
    int L;
    scanf("%d", &L);
    int power = 1 << (L - 1);
    int result = 0;

    while (1) {
        char nextBit;
        scanf("%c", &nextBit);
        if (nextBit == ' ') {
            continue;
        }

        // Your code here!
        if (nextBit == '1') {
            result += power;
        } else if (nextBit == '0') {

        } else {
            break;
        }
        power = power / 2;
    }

    printf("%d", result);

    // Keep this return 0;
    return 0;
}