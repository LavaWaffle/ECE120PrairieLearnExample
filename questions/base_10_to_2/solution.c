#include <stdio.h>

int main() {
    // Get N
    int N;
    scanf("%d", &N); // N is between 0 and 63.

    int power_of_two = 32;

    while (power_of_two > 0) {
        if (N >= power_of_two) {
            printf("1");
            N -= power_of_two;
        } else {
            printf("0");
        }
        power_of_two /= 2;
    }

    printf("\n");
    return 0;
}