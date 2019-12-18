#ifndef sailboat_H
#define sailboat_H

#include <string>



class Sailboat
{
public :

Sailboat();
void avancer();
void suivideligne();



double x,y,v,theta,omega; // state variables x,y : position ; v : vitesse ; theta : cap ; omega : variation de cap
double beta, alphag; // parametres beta : coeff dérive ; alphag : coeff de portance du gouvernail ; deltag : angle du gouvernail
double a,psi; // wind a : vitesse ; psi : angle
double dt;  // pas
//double fg;  //link variables  fg : force de l'eau sur le gouvernail

double ax,ay,bx,by; ///point A et point B/////
double e; ///ecart au cap///
};


#endif // sailboat_H
