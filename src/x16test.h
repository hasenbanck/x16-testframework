#ifndef _X16TEST_H
#define _X16TEST_H
#include <stdlib.h>
#include <stdlib.h>

extern void quit(unsigned char status);

#define START_TEST int main(void) \
{

#define END_TEST    quit(0);\
    return EXIT_SUCCESS;\
}

#define ASSERT(a)    if (!(a)) {\
        printf("assertion failed at %s:%d\n",__FILE__, __LINE__);\
        quit(1);\
    }

#endif
