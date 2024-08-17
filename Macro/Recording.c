#include <stdio.h>
#include <conio.h>
#include <State.h>

int main() {
    char Input = getch();
    FILE *SaveFile = fopen(SaveFileName, "w");

    if (SaveFile == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    while (Input != 27) {
        fprintf(SaveFile, "%c", Input);
        Input = getch();
    }

    fclose(SaveFile);

    return 0;
}
