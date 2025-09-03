#include <stdio.h>

// Harder solution that makes student think like LC-3 Version of this conversion.

// Convert from base 2 to base 16
int main() {
    int latest_result = 0;
    int cur_power = 1 << 3; // 8 (MSB of a 4 bit segment)
    int processed_bits = 0;

    while (1) {
        char nextBit;
        scanf("%c", &nextBit);

        if (nextBit == '1') {
            latest_result += cur_power;
        } else if (nextBit != '0') {
            // EOS
            break;
        }
        processed_bits++;
        cur_power = cur_power / 2;

        if (processed_bits % 4 == 0) {
            printf("%X", latest_result);
            latest_result = 0;
        }
    }

    // Keep this return 0;
    return 0;
}