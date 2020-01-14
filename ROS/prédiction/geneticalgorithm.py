#le but de cet algorithme est de trouver le plus cours chemin entre 2 waypoint. 
import numpy as np 
import random
import math

class ga :
    def __init__(self, nbwaypoints :int, nbCellules:int, nbGenerations:int, fctCout:"fonction", A:"porte", B:"porte", largeurRoute:float):
        self.nbwaypoints=nbwaypoints
        self.nbCellules=nbCellules
        self.nbGenerations=nbGenerations
        self.generation=np.zeros((nbwaypoints+1,nbCellules,2*nbGenerations)) #chaque génération est sur 2 lignes : 1er : génération, 2em élimination la dernière colonne du nb de waypoint
        self.fctCout=fctCout
        self.A=A                                            #point initial [[x1, y1],[x2, y2]] chaques points est une porte
        self.B=B                                            #point final
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        self.Am=[(A[0][0]+A[1][0])/2, (A[0][1]+A[1][1])/2]  #centre de la porte
        self.Bm=[(B[0][0]+B[1][0])/2, (B[0][1]+B[1][1])/2]

    def fctgeneration(self):
        ### 1er génération
        for k in range(self.nbCellules):                                #on crée les premières cellules                                
            gen0k=self.tirageCoordonnee()                               
            self.generation(self.nbwaypoints,0,k)=self.fctCout(gen0k)   #la dernière case est le cout
            for i in range(nbwaypoints):
                self.generation(i,0,k)=gen0k[i]                         #on rentre les cellules dans la matrice
        
        c=choixCellules(0, self.nbCellules//2,1)                        #choix des cellules 
        while len(c)<self.nbCellules:                                   #on complète aléatoirement les cellules manquante
            c.append(random.choices(c, k=1))
        for j in range(len(c)):                                         #on copie les cellules
            for i in range(self.nbwaypoints)                                        
            self.generation(i,j,1)=self.generation(i,j,0)
        
        for i in range(1, self.nbGenerations):
            #on évolue puis on choisi
            j=i

    
    def choixCellules(self, j:int, k:int, m:int)->list:
        """prend le numéro de génération (j) et choisi les numéros des k cellules à garder 
        en utilisant la methode m:
        1 : Sélection par rang (on prend les k meillieurs)
        2 : Probabilité de sélection proportionnelle à l'adaptation (on en prend k aléatoirement prépondérant a sa fct cout)
        3 : Sélection par tournoi 1vs1 jusqu'a ce qu'il en reste k
        4 : Sélection uniforme
        """
        T=[self.generation(self.nbwaypoints,i,j) for i in range(self.nbCellules)]
        if(m==1):#trie sur les indices
            TT=zip(T, xrange(len(T)))
            TT.sort()
            T=[x for (x,y) in TT]
            indice=[y for (x,y) in TT]

            return indice(:k-1)

        elif(m==2):
            somme=sum(T)
            T=[T[i]/somme for i in range(self.nbCellules)]
            for i in range(1,len(T)):
                T[i]+=T[i-1]
            T[0]=0
            #T devient une liste croisante entre 0 et 1-T[-1] 
            retour=[]
            for i in range(k):
                r=random.random()
                l=0
                while T[l]<r:
                    l+=1
                retour.append(l-1)

        elif(m==3):
            indice=[i for i in range(self.nbCellules)]
            while len(indice)<k:            #complexite nbCellule-k
                t=random.choices(indice,k=2)
                if(T[t[0]]>T[t[1]]):
                    indice.pop(t[1])
                else:
                    indice.pop(t[0])
            return indice

        else:  
            retour=random.choices([i for i in range(self.nbCellules)],k=k)


    def tirageCoordonnee(self)->"list float":
        """comme le tirage doit rester dans la route, on choisi une distance sur l'axe, puis un ecartement par rapport a la route,
        puis cela est converti en cartesien
        la liste des waypoints est genérer en même temps, le iem point se place aléatoirement dans l'interval [i*longeurRouteDirecte/nbwaypoints, (i+1)*longeurRouteDirecte/nbwaypoints]
        """
        longeurRouteDirecte=math.sqrt((Am[0]-Bm[0])**2+(Am[1]-Bm[1])**2)

        retour=[]
        for i in range(self.nbwaypoints):
            retour.append([random.randrange(i*longeurRouteDirecte/nbwaypoints, (i+1)*longeurRouteDirecte/nbwaypoints), random.randrange(-self.largeurRoute/2, self.largeurRoute/2)])
        
        theta=math.atan2(Am[1]-Bm[1],Am[0]-Bm[0])

        for i in range(len(retour)): 
            alpha=theta+math.atan2(retour[i][1],retour[i][0])               #vérifier les angles !
            distance=math.sqrt(retour[i][0]**2+retour[i][1]**2)
            retour[i]=[Am[0]+distance*math.cos(alpha), Am[1]+distance*math.sin(alpha)]
        
        
        return retour

    def evolution(self):
        return None