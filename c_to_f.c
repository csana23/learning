#include <stdio.h>

/*this is a comment*/

float c = -40.0;
float max_c = 100.0;

int main() {

    while (c < max_c) {
        
        float f = c*(9.0/5.0)+32.0;
        printf("%f\t%f\n", c, f);
        c = c + 10.0;

        //printf("%s", "this is a string");

       
        
    }

    return 0;
}