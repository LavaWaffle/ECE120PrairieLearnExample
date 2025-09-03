#include <stdio.h>

// Convert from base 2 to base 16
int main() {
    int result = 0;
    int cur_power = 1 << 7; // 128 (MSB of a 8 bit unsigned binary)

    while (1) {
        char nextBit;
        scanf("%c", &nextBit);

        if (nextBit == '1') {
            result += cur_power;
        } else if (nextBit != '0') {
            // EOS
            break;
        }
        cur_power = cur_power / 2;
    }
    printf("%X", result);

    // Keep this return 0;
    return 0;
}