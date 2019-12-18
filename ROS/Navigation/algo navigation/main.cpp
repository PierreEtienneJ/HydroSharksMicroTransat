#include <iostream>
#include "sailboat.h"
#include "CImg.h"
#include <vector>

using namespace cimg_library;
using namespace std;



int main()
{

Sailboat hydrosharks;  ///Création de 1 bateau

vector<double> X(1); ///tableau des coordonnées du bateau///
vector<double> Y(1);

///Initialisation///

X[0]=hydrosharks.x;
Y[0]=hydrosharks.y;


CImg<int> img(1000, 1000, 1, 1,0); /// image noire


const unsigned char blanc[] = {255, 255,255}; ///definition du blanc
const unsigned char noir[] = {0, 0,0}; ///definition du noir
CImg<int> bateau("bateau.png"); ///chargemrnt de l'image du bateau

img.draw_rectangle(0, 0, 1950, 1950, blanc); ///dessin du fond blanc

///Parcours/////////
for (int i=0; i<2500;i++)
{

hydrosharks.suivideligne();
hydrosharks.avancer();

X.push_back(hydrosharks.x);///recolte des nouvelles coordonnees
Y.push_back(hydrosharks.y);


std::cout << hydrosharks.x<< std::endl;///affichage
std::cout << hydrosharks.y<< std::endl;
}

int N=0;
N=X.size(); ///taille du tableau de coordonnees

img.draw_line(hydrosharks.ax,hydrosharks.ay,hydrosharks.bx,hydrosharks.by,noir);///dessin de la ligne que le bateau doit suivre
img.draw_arrow(50,50,50+50*cos(hydrosharks.psi),50+50*sin(hydrosharks.psi),noir,1,30,-60);///fleche du vent
for (int j=0;j<N;j++)
{
img.draw_circle(X[j], Y[j], 2, noir);///tracé du trajet du bateau

}
img.draw_image(100,100,0,0,bateau);///dessin bateau
img.display();///affichage de l'image
return 0;



}
