import math as m
T=5*3600
dt=30
tetamin=10
dteta=10
R=2000
# ALERTE !!!!!! Ce code ne marche pas si à un instant t, il a soit 2 bateaux qui posent pb, soit si après modif ça pose pb

def CalculTrajectoireEux(AIS,T,dt):
    # Cette fonction permet de créer la matrices avec les [lat,long] pour les différents instants futurs des bateaux
    # AIS sera une liste avec chaque élément de la forme : [lattitude,longitude,vitesse,cap] pour chaque obstacle
    # T est le tps total de vérification, dt le pas de temps
    F=[[[0,0]]*len(AIS)]*T/dt
    for t in range (2,T+1,dt):
        
        for i in range (len(AIS)):
            
            F[t-2][i]=[AIS[0]+t*AIS[2]*m.cos(m.radians(AIS[3])),AIS[0]+t*AIS[2]*m.sin(m.radians(AIS[3]))]
            
    return(F)
    
def CalculTrajectoireNous(NOUS,T,dt):
    # Cette fonction permet de créer la matrice avec les [lat,long] pour les différents instants futurs de notre bateau
    # NOUS sera une liste avec chaque élément de la forme : [lattitude,longitude,vitesse,cap] pour chaque instant
    # NOUS ce sera la même chose mais pou notre bateau
    # T est le tps total de vérification, dt le pas de temps
    N=[[0,0]]*T/dt
    
    for t in range (2,T+1,dt):
        
        N[t-2]=[NOUS[0]+t*NOUS[2]*m.cos(m.radians(NOUS[3])),NOUS[0]+t*NOUS[2]*m.sin(m.radians(NOUS[3]))]
            
    return(N)
    
def couragefuyons(NOUS,Fti,Nti,T,dt,R,teta) :
    # Code qui nous permets de changer notre trajectoire 
    # Il prend les coord de nous et du bateau qui pose pb et renvoie le nouveau NOUS (cap changé)
    if m.acos(Nti[0]/t*NOUS[2])<=m.pi:
        
        while m.sqrt((Nti[0]-Fti[0])^2+(Nti-Fti[1])^2)<2*R:
            
            NOUS[3]+=teta
            
            if NOUS[3]>360:
                NOUS[3]-=360
                
        return(NOUS)
        
    elif m.acos(Nti[0]/t*NOUS[2])>m.pi:
        
        while m.sqrt((Nti[0]-Fti[0])^2+(Nti[1]-Fti[1])^2)<2*R:
            
            NOUS[3]-=teta
            
            if NOUS[3]<0:
                NOUS[3]+=360
                
        return(NOUS)
    

def alertecollision(NOUS,AIS,F,N,T,dt,R,tetamin,dteta):
    # Cette fonction permet de vérifier si il y a collision avec les bateaux et les éviter
    # Elle renvoit une matrice de [CAP(t),t] pour chaque instant vérifié
    NOUSbis=NOUS
    NOUSbisbis=[0]*len(NOUS)
    CAP=[0,0]*T/dt
    c=0
    
    for t in range (2,T+1,dt):
        for i in range (len(AIS)):
            
            NOUSbis=couragefuyons(NOUSbis,F[t-2],N[t-2][i],T,dt,R,tetamin)
        
            while NOUSbis[3]!=NOUSbisbis[3]:
                
                if c<=2*len(AIS):
                    
                    NOUSbisbis=NOUSbis
                    NOUSbis=couragefuyons(NOUSbis,F[t-2],N[t-2][i],T,dt,R,tetamin)
                    
                elif c>2*len(AIS) and c<=4*len(AIS):
                    
                    NOUSbisbis=NOUSbis
                    NOUSbis=couragefuyons(NOUSbis,F[t-2],N[t-2][i],T,dt,R,tetamin+dteta)
                    
                else :
                    
                    NOUSbisbis=NOUSbis
                    NOUSbis=couragefuyons(NOUSbis,F[t-2],N[t-2][i],T,dt,R,tetamin+2*dteta)
                    
                c+=1    
            
        CAP[t-2][0]=t-2
        CAP[t-2][1]=NOUSbis[3]
    return(CAP)