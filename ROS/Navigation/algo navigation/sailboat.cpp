#include "sailboat.h"
#include "math.h"

using namespace std;

Sailboat::Sailboat() /// Initialisation
{
///Position initiale////
    x = 20;
    y = 950;
///Vitesse initiale///
    v = 1;
///Cap initial////
    theta = 3.0;
///Coeff de dérive////
    beta = 0.1;
///vitesse du vent////
    a = 4 ;
///angle du vent///
    psi = (3*3.14)/4;
///pas///
    dt = 0.1;
///variation de cap///
    omega = 0.0;
///portance du gouvernail
    alphag = 2000.0;
///portance de la voile
    alphav= 1000.0;
    ///Point A/////
    ax = 10; ay = 990;
    ///Point B/////
    bx = 950; by = 10;
    ///ecart au cap///
    e = 0;
///moments d'inertie///
    Jz = 10000.0;
    Jx = 3000.0;
///distance entre le centre de poussée de la voile et le mat
    l=1.0;
/// distance du mat a G
    rv=1.0;
///distance du gouvernail a G
    rg=2.0;
///coefficient angulaire de frottement
    alphatheta=6000;
///masse du bateau
    m=300.0;
///coefficient de frottement trainee
    alphaf = 1.0;
///variation de phi
    phiPoint = 0;
/// hauteur de centre de poussée
    hv = 4.00;
///angle de la ligne
    phi = 0.5;


    q=1;
}

double sign(double a)
{if (a>0) return 1; else return -1;};

void Sailboat::avancer()
{

double xw_ap=a*cos(psi-theta)-v;
double yw_ap=a*sin(psi-theta);
double psi_ap=atan2(yw_ap,xw_ap);   //Apparent wind
double a_ap=sqrt(xw_ap*xw_ap+yw_ap*yw_ap);
gamma=cos(psi_ap)+cos(deltavmax);
if (gamma<0) {deltav=M_PI+psi_ap;} //voile en drapeau
else  if (sin(-psi_ap)>0) deltav=deltavmax;   else deltav=-deltavmax;
fg = alphag*v*sin(deltag);
fv = alphav*a_ap*sin(deltav-psi_ap);

x += (v*cos(theta)+beta*a*cos(psi))*dt;
y += (v*sin(theta)+beta*a*sin(psi))*dt;
theta += omega*dt;


omega += (1/Jz)*((l-rv*cos(deltav))*fv-rg*cos(deltag)*fg-alphatheta*omega*v)*dt;
v += (1/m)*(sin(deltav)*fv-sin(deltag)*fg-alphaf*v*v)*dt;
phiPoint += (-phiPoint+fv*hv*cos(deltav)*cos(phi)/Jx - 10000*9.81*sin(phi)/Jx)*dt ;
phi += phiPoint * dt;


}

void Sailboat::suivideligne()
{
double r=50; ///ecart a la ligne accepté///
double zeta=M_PI/4;
e=((bx-ax)*(y-ay)-(x-ax)*(by-ay))/hypot(ax-bx,ay-by); ///calcul de l'écart a la ligne///
if (fabs(e)>r) q=0; ///si l'écart est trop important///
double phi=atan2(by-ay,bx-ax); ///angle de la ligne///
double thetabar=phi-0.5*atan(e/r);///cap tenable///
if ((q==0)&((cos(psi-thetabar)+cos(zeta)<0)|((fabs(e)<r)&(cos(psi-phi)+cos(zeta)<0))))
    {
    q=sign(e);
    }
theta += omega*dt;
omega += (1/Jz)*((l-rv*cos(deltav))*fv-rg*cos(deltag)*fg-alphatheta*omega*v)*dt;
v += (1/m)*(sin(deltav)*fv-sin(deltag)*fg-alphaf*v*v)*dt;
phiPoint += (-phiPoint+fv*hv*cos(deltav)*cos(phi)/Jx - 10000*9.81*sin(phi)/Jx)*dt ;
phi += phiPoint * dt;
if (q!=0)
  {
  thetabar=M_PI+psi-zeta*q;
  }
double dtheta=theta-thetabar;
deltag=(1/M_PI)*(atan(tan(0.5*dtheta)));
deltavmax=0.5*M_PI*(0.5*(cos(psi-thetabar)+1));

}


