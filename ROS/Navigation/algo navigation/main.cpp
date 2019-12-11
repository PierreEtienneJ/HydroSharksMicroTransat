#include <iostream>
#include "sailboat.h"

using namespace std;



int main()
{
int i=0;
Sailboat hydrosharks;
    //Création de 1 bateau

///////Parcours/////////
for (i=0; i<10;i++)
{

hydrosharks.suivideligne();
hydrosharks.avancer();
std::cout << hydrosharks.x<< std::endl;
}

    return 0;



}
