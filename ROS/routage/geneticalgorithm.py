#le but de cet algorithme est de trouver le plus cours chemin entre 2 waypoint. 
import numpy as np
import random
import math
import matplotlib.pyplot as plt

class Ga :
    def __init__(self, A:"depart", B:"porte arrivee", largeurRoute:float):
        self.nbwaypoints=0                                  #nb de points par cellules
        self.nbCellules=0                                   #nb de cellules de l'algo
        self.nbGenerations=0                                #nb de génération
        self.generation=np.zeros((2,self.nbwaypoints+1,self.nbCellules,2*self.nbGenerations)) #chaque génération est sur 2 lignes : 1er : génération, 2em élimination la dernière colonne du nb de waypoint
        self.A=A                                            #point initial 
        self.B=B                                            #point final [[x1, y1],[x2, y2]]
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        self.Am=A                                           #centre de la route
        self.Bm=[(B[0][0]+B[1][0])/2, (B[0][1]+B[1][1])/2]  

    def fctgeneration(self,nbwaypoints :int, nbCellules:int, nbGenerations:int, mEvol:int, mChoix:int):
        self.nbwaypoints=nbwaypoints                 
        self.nbCellules=nbCellules
        self.nbGenerations=nbGenerations
        self.generation=np.zeros((2,self.nbwaypoints+1,self.nbCellules,2*nbGenerations)) 
        #chaque génération est sur 2 lignes : 1er : génération, 2em élimination la dernière colonne du nb de waypoint

        ### 1er génération
        for k in range(self.nbCellules):                                #on crée les premières cellules                                
            gen0k=self.tirageCoordonnee()                               #tire les 1er waypoints
            for i in range(nbwaypoints):
                self.generation[0,i,k,0]=gen0k[i][0]                         #on rentre les cellules dans la matrice
                self.generation[1,i,k,0]=gen0k[i][1]
            self.generation[0,self.nbwaypoints,0,k]=self.fctCout(k, 0) #la dernière case est le cout
        


        for k in range(0, self.nbGenerations,2):
            #choix des cellules 
            c=self.choixCellules(k, self.nbCellules//2+1,mChoix)               
            # on copie les première cellules cela permet de mieux suivre l'évolution
            for j in range(len(c)):                               
                for i in range(self.nbwaypoints):                                        
                    self.generation[0,i,c[j],k+1]=self.generation[0,i,c[j],k]
                    self.generation[1,i,c[j],k+1]=self.generation[1,i,c[j],k]

            for j in range(self.nbCellules):   #on complète l'algo
                for i in range(self.nbwaypoints):   
                    if(self.generation[0,i,j,k+1]==0.00 and self.generation[1,i,j,k+1]==0.00): #si la cellule n'est pas garder à la génération k                                  
                        l=random.choices([i for i in range(self.nbCellules)],k=1)
                        self.generation[0,i,j,k+1]=self.generation[0,i,l[0],k]
                        self.generation[1,i,j,k+1]=self.generation[1,i,l[0],k]
                self.generation[0,self.nbwaypoints,j,k]=self.fctCout(j, k)
            #self.affichegen(k+1)

            #EVOLUTION
            self.evolution(k+1, mEvol)  #évolution avec une certaine méthode

            #calcul du cout de chaque cellules
            for j in range(self.nbCellules): 
                self.generation[0,self.nbwaypoints,j,k+1]=self.fctCout(j, k+1)   #calcul du cout
            

    def choixCellules(self, j:int, k:int, m:int)->list:
        """prend le numéro de génération (j) et choisi les numéros des k cellules à garder 
        en utilisant la methode m:
        1 : Sélection par rang (on prend les k meilleurs)
        2 : Probabilité de sélection proportionnelle à l'adaptation (on en prend k aléatoirement prépondérant a sa fct cout)
        3 : Sélection par tournoi 1vs1 jusqu'a ce qu'il en reste k
        4 : Sélection uniforme
        """
        T=[self.generation[0,self.nbwaypoints,i,j] for i in range(self.nbCellules)] #liste des couts
        
        if(m==1):#trie sur les indices
            T=[[T[i],i] for i in range(self.nbCellules)] #liste des couts avec indice
            element = lambda T: T[0]
            T=sorted(T,key=element,reverse=False) #on fait le trie sur la 1er colone de la matrice
            indice=[T[i][1] for i in range(len(T))] #on sort les indices

            return indice[0:k-1] #on en garde que k

        elif(m==2):
            somme=sum(T)
            T=[T[i]/somme for i in range(self.nbCellules)] #liste des couts prépondéré 
            for i in range(1,len(T)):
                T[i]+=T[i-1]
            T[0]=0
            #T devient une liste croisante entre 0 et 1-T[-1] 
            retour=[]
            for i in range(k):
                r=random.random()
                l=0
                while T[l]<r: #vérifier l'inégalité
                    l+=1
                retour.append(l-1)
            return retour
            
        elif(m==3):
            indice=[i for i in range(self.nbCellules)]
            while len(indice)<k:            #complexite nbCellule-k
                t=random.choices(indice,k=2) #prend 2 cellules
                if(T[t[0]]<T[t[1]]): #regarde la plus forte (forte=cout plus petit)
                    indice.pop(t[1])    #la plus forte reste 
                else:
                    indice.pop(t[0])
            return indice

        else:  
            return random.choices([i for i in range(self.nbCellules)],k=k) #choix alléatoire


    def tirageCoordonnee(self)->"list float":
        """comme le tirage doit rester dans la route, on choisi une distance sur l'axe, puis un ecartement par rapport a la route,
        puis cela est converti en cartesien
        la liste des waypoints est genérer en même temps, le iem point se place aléatoirement dans l'interval [i*longeurRouteDirecte/nbwaypoints, (i+1)*longeurRouteDirecte/nbwaypoints]
        
        Pour le moment c'est linéaire mais la densité deviendra en exp(-x)
        """
        longeurRouteDirecte=math.sqrt((self.Am[0]-self.Bm[0])**2+(self.Am[1]-self.Bm[1])**2)
        theta=math.atan2(self.Am[0]-self.Bm[0],self.Am[1]-self.Bm[1])
        retour=[]
        
        for i in range(self.nbwaypoints):
            r=[random.random()*longeurRouteDirecte/self.nbwaypoints+i*longeurRouteDirecte/self.nbwaypoints, random.random()* self.largeurRoute-self.largeurRoute/2]
            alpha=theta+math.atan2(r[0],r[1])               #vérifier les angles !
            distance=math.sqrt(r[0]**2+r[1]**2)             #chagement de repère
            r=[self.Am[0]+distance*math.cos(alpha), self.Am[1]-distance*math.sin(alpha)]
            retour.append(r)
        return retour

    def evolution(self, igen:int, m:int):
        """igen : numéro de la génération en cours
        m : méthode d'évolution
        1: translation aléatoire
        2: fusion cellulaire
        """
        coef=0.1
        if(m==1): #on deplace chaque point de [-coef; coef]
            for i in range(self.nbCellules):
                for j in range(self.nbwaypoints):
                    T=[self.generation[0,j, i, igen], self.generation[1,j, i, igen]] #liste des points
                    T[0]=T[0]+random.random()*2*coef-coef #translation des points
                    T[1]=T[1]+random.random()*2*coef-coef

                    self.generation[0,j, i, igen+1]=T[0]      #on crée la génération suivante
                    self.generation[1,j, i, igen+1]=T[1]      #on crée la génération suivante
        elif(m==2): #fuision cellulaire : on prend deux cellules et on mixe certaine cellules dans les deux cellules
            probaFusionWaypoint=10/100  #proba de fusion
            for i in range(0,self.nbCellules,2):
                for j in range(self.nbwaypoints):
                    if(probaFusionWaypoint<random.random()):
                        T=[self.generation[0,j, i, igen], self.generation[1,j, i, igen]] #waypoint cellule i de la genération courante
                        L=[self.generation[0,j, i+1, igen], self.generation[1,j, i+1, igen]] #waypoint cellule i+1
                        K=[(T[0]+L[0])/2,(T[1]+L[1])/2]      #moyenne des waypoints
                        self.generation[0,j, i, igen+1]=K[0] #save le nouveau points sur une des deux cellules
                        self.generation[0,j, i+1, igen+1]=L[0]
                        self.generation[1,j, i, igen+1]=K[1]
                        self.generation[1,j, i+1, igen+1]=L[1]
            

    def fctCout(self, kCellule:int, igen:int)->float:
            s=0 #longueur du chemin
            p=self.Am
            for j in range(self.nbwaypoints):
                w=[self.generation[0,j, kCellule, igen], self.generation[1,j, kCellule, igen]]
                s+=math.sqrt((w[0]-p[0])**2+(w[1]-p[0])**2)
                #if(-5<w[0]<5 and -5<w[1]<5):
                 #   s+=10
                p=w
            w=self.Bm    
            s+=math.sqrt((w[0]-p[0])**2+(w[1]-p[0])**2)
            return s
    
    def affiche(self, kCellule:int):
        Xa=[]
        Ya=[]
        Xb=[]
        Yb=[]
        Xc=[]
        Yc=[]
        Xd=[]
        Yd=[]
        Xe=[]
        Ye=[]
        Xf=[]
        Yf=[]
        for i in range(self.nbwaypoints):
            Xa.append(self.generation[0,i,0,self.nbGenerations-1])
            Ya.append(self.generation[1,i,0,self.nbGenerations-1])
            Xb.append(self.generation[0,i,1,self.nbGenerations-1])
            Yb.append(self.generation[1,i,1,self.nbGenerations-1])
            Xc.append(self.generation[0,i,2,self.nbGenerations-1])
            Yc.append(self.generation[1,i,2,self.nbGenerations-1])

            Xd.append(self.generation[0,i,3,self.nbGenerations-1])
            Yd.append(self.generation[1,i,3,self.nbGenerations-1])
            Xe.append(self.generation[0,i,4,self.nbGenerations-1])
            Ye.append(self.generation[1,i,4,self.nbGenerations-1])
            Xf.append(self.generation[0,i,5,self.nbGenerations-1])
            Yf.append(self.generation[1,i,5,self.nbGenerations-1])
        
        Xa.append(self.Bm[0])
        Ya.append(self.Bm[1])
        Xb.append(self.Bm[0])
        Yb.append(self.Bm[1])
        Xc.append(self.Bm[0])
        Yc.append(self.Bm[1])

        Xd.append(self.Bm[0])
        Yd.append(self.Bm[1])
        Xe.append(self.Bm[0])
        Ye.append(self.Bm[1])
        Xf.append(self.Bm[0])
        Yf.append(self.Bm[1])
        
        print(Xa)
        print(Xb)
        print(Xc)
        print(Xd)
        print(Xe)
        print(Xf)
        print(self.generation[0,self.nbwaypoints, 0, 1])
        print(self.generation[0,self.nbwaypoints, 0, self.nbGenerations//2])
        print(self.fctCout(0, self.nbGenerations-1))
        print(self.generation[0,self.nbwaypoints, 1, 1])
        print(self.generation[0,self.nbwaypoints, 1, self.nbGenerations//2])
        print(self.fctCout(1, self.nbGenerations-1))
        plt.plot(Xa,Ya,'g-',Xb,Yb,'b-',Xc,Yc,'r-',Xd,Yd,'y-',Xe,Ye,'m-',Xf,Yf,'w-')
        plt.show()
        
        #best=self.resultat()
        #Xbest=[best[i][0] for i in range(self.nbwaypoints)]
        #Ybest=[best[i][1] for i in range(self.nbwaypoints)]
        #plt.plot(Xbest, Ybest)
        #plt.show()
        
        X=[]
        for i in range(self.nbCellules):
            Y=[]
            for j in range(self.nbGenerations):
                Y.append(self.generation[0,self.nbwaypoints, i, j])
            X.append(Y)
        Y=[i for i in range(self.nbGenerations)]    
        plt.plot(Y,X[0],'g',Y,X[1],'r',Y,X[2],'b')
        plt.show()

    def affichegen(self, igen:int):
        for j in range(self.nbCellules):
            print("///"+str(j+1)+"//////////////////////////////")
            print(self.generation[0,self.nbwaypoints,j,igen])
        print("##############")
    
    def resultat(self):
        best=self.generation[0,self.nbwaypoints,0,self.nbGenerations-1]
        i=0
        for j in range(1,self.nbCellules):
            if(best>self.generation[0,self.nbwaypoints,j,-1]):
                i=j
                best=self.generation[0,self.nbwaypoints,j,-1]
        retour=[]
        for k in range(self.nbwaypoints):
            retour.append([self.generation[0,k,i,-1], self.generation[1,k,i,-1]])
        return retour

if __name__ == "__main__":
    #carte=np.random.rand(100,100)
    ga=Ga([10,0], [[10,9],[10,11]], 5)
    ga.fctgeneration(10,100,100,2,4)  #2,2 meillieur, plus rapide  100 100 100 #1, 2 pas bon
    ga.affiche(0)


