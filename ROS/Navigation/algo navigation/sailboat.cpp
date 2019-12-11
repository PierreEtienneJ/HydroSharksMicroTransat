#include "sailboat.h"
#include "math.h"

using namespace std;

Sailboat::Sailboat() // Initialisation
{
////Position initiale////
    x = 0;
    y = 0;
////Vitesse initiale///
    v = 1;
////Cap initial////
    theta = 3.0;
////Coeff de dérive////
    beta = 0.1;
////vitesse du vent////
    a = 2 ;

    psi = M_PI;
    dt = 0.1;
    omega = 0.0;
    alphag = 2000.0;
    /////Point A/////
    ax = -1000; ay = -2000;
    ////Point B/////
    bx = 1000; by = 2000;
    ///ecart au cap///
    e = 0;
}

double sign(double a)
{if (a>0) return 1; else return -1;};

void Sailboat::avancer()
{

x += (v*cos(theta)+beta*a*cos(psi))*dt;
y += (v*sin(theta)+beta*a*sin(psi))*dt;
theta += omega*dt;
//fg = alphag*v*sin(deltag);


}

void Sailboat::suivideligne()
{
double r=10; ///ecart a la ligne accepté///
///double zeta=M_PI/4;
e=((bx-ax)*(y-ay)-(x-ax)*(by-ay))/hypot(ax-bx,ay-by); ///calcul de l'écart a la ligne///
///if (fabs(e)>r) q=0; ///si l'écart est trop important///
double phi=atan2(by-ay,bx-ax); ///angle de la ligne///

}


