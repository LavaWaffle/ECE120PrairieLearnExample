#include <stdio.h>
void print_binary(const char* label, double num);

// open terminal: ctrl + ~
// compile: gcc starter_code.c -o starter_code -lm
// execute: ./starter_code
int main() {
    double a = 0.1 + 0.2;
    double b = 0.3;

    printf("0.1 + 0.2 == 0.3: %d\n", a == b);

    return 0;
}













// Ignore this code for now (you'll learn all this in ECE 220)
// Feel free to ask in ECE 120 OH if you'd like to know more about how this works, but none of the below will be tested on exams.
#include <stdint.h>

typedef union {
    double d;
    uint64_t u;
} DoubleUnion;

void print_binary(const char* label, double num) {
    DoubleUnion converter;
    converter.d = num;

    printf("%-10s: ", label);
    
    // Iterate from the most significant bit (63) down to the least significant (0)
    for (int i = 63; i >= 0; i--) {
        // Create a mask with a 1 at the i-th position
        uint64_t mask = 1ULL << i; 
        
        // Use bitwise AND to check if the bit is set
        printf("%c", (converter.u & mask) ? '1' : '0');

        // Add spaces for readability to separate sign, exponent, and mantissa
        // For a double: 1 sign bit, 11 exponent bits, 52 mantissa bits
        if (i == 63 || i == 52) {
            printf(" ");
        }
    }
    printf("\n");
}