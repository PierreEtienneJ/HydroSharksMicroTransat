#ifndef sailboat_H
#define sailboat_H

#include <string>


class Sailboat
{
    public :

    Sailboat();
    void avancer();
    void suivideligne();



    double x,y; ///position
    double v; ///vitesse
    double theta,omega; ///cap et variation de cap
    double phi,phiPoint; /// angle de la ligne et variation de l'angle de la ligne
    double beta,alphag,alphav,alphaf,alphatheta; ///coeff de dérive, portance du gouvernail, portance de la voile, frottement de trainee, frottement angulaire
    double l,rv,rg; /// distance entre le centre de poussée de la voile et le mat,  distance du mat a G, distance du gouvernail a G
    double m; ///masse
    double Jz, Jx; /// moments d'inertie
    double a,psi; /// vent a : vitesse  psi : angle
    double dt;  /// pas
    double fv,fg,gamma,deltav,deltag,deltavmax;  /// deltag : angle de la voile  fg : force de l'eau sur le gouvernail fv : force du vent sur la voile, deltav  : angle de la voile

    double ax,ay,bx,by; ///point A et point B/////
    double e; ///ecart au cap///
    double hv;

    int q;
};


#endif // sailboat_H
