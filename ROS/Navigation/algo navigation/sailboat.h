#ifndef sailboat_H
#define sailboat_H

#include <string>


class Sailboat
{
public :

Sailboat();
void avancer();
void suivideligne();



double x,y,v,theta,omega,phiPoint,phi; // state variables x,y : position  v : vitesse theta : cap omega : variation de cap
double beta,Jz,l,rv, rg,alphag,alphav,alphaf,alphatheta,m,Jx; // parameters beta : coeff dérive alphag : coeff de portance du gouvernail deltag : angle du gouvernail
double a,psi; // wind a : vitesse  psi : angle
double dt;  // pas
double fv,fg,gamma,deltav,deltag,deltavmax;  //link variables deltag : angle de la voile  fg : force de l'eau sur le gouvernail

double ax,ay,bx,by; ///point A et point B/////
double e; ///ecart au cap///
double hv;

int q;
};


#endif // sailboat_H
