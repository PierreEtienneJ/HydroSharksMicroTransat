import numpy as np
import random
import math
import matplotlib.pyplot as plt
import statistics
import time
import map
import threading
import sys
import folium 


def g(v:float,theta:float): # vitesse bateau en fct du vent
    if(-5<theta<5):
        x= 0
    elif(-20<theta<20):#hormis [-5, 5]
        if(theta>0):
            #coef droite
            A=np.array(([5,1],[20, 1]))
            Y=np.array((0, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            x=a*theta+b
        else:
            A=np.array(([-5,1],[-20, 1]))
            Y=np.array((0, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            x=a*theta+b            
    else:
        if(theta>0):
            A=np.array(([100**2, 100, 1],[180**2, 180, 1], [20**2, 20, 1]))
            Y=np.array((4, 2, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            c=X[2]
            x=a*theta**2+b*theta+c
        else:
            A=np.array(([100**2, -100, 1],[180**2, -180, 1], [20**2, -20, 1]))
            Y=np.array((4, 2, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            c=X[2]
            x=a*theta**2+b*theta+c
    v=abs(v)
    #A=np.array(([30**2, 30, 1],[10**2, 10, 1], [50**2, 50, 1]))
    #Y=np.array((4, 1, 3))
    A=np.array(([0, 0, 1],[30**2, 30, 1], [80**2, 80, 1]))
    Y=np.array((0, 20, 3))
    X=np.dot(np.linalg.inv(A),Y)
    a=X[0]
    b=X[1]
    c=X[2]
    y=a*v**2+b*v+c
    return abs(x*y)/10

def e(vent:float, uv:int): #conso, prod en fonction de la météo
    return [vent/2+10, (2*uv**2+uv+10)/10] 
    
class StopGA(threading.Thread):
    def __init__(self, tarret:float, ga):
        threading.Thread.__init__(self)
        self.verrou=False
        self.time=0
        self.tmax=tarret
        self.ga=ga
    def run(self):
        t0=time.time()
        self.time=time.time()-t0
        while(self.ga.isRun): 
            if(self.tmax!=None):
                if(self.time>self.tmax): #condition de fin de la GA
                    self.verrou=True
                    sys.stdout.write("demande stop ga")
                    sys.stdout.flush()
                
        sys.stdout.write("ga was stop \n")
        sys.stdout.flush()
        
class Ga(threading.Thread):
    def __init__(self, C:"depart reel", A:"depart th", B:"porte arrivee", largeurRoute:float, stopGa:StopGA):
        """A,B,C en lat/long"""
        threading.Thread.__init__(self)
        
        self.nbwaypoints=None                                  #nb de points par cellules
        self.nbCellules=None                                   #nb de cellules de l'algo
        self.nbGenerations=None                                #nb de génération
        self.generation=None
        self.A=A                                            #point initial théorique 
        self.C=C    #pts initial
        self.B=B                                            #porte finale [[x1, y1],[x2, y2]]
        self.A=map.sexagesimauxToDecimaux2(self.A)
        self.C=map.sexagesimauxToDecimaux2(self.C)
        self.B[0]=map.sexagesimauxToDecimaux2(self.B[0])
        self.B[1]=map.sexagesimauxToDecimaux2(self.B[1])
        
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        [x0,y0]=map.gpsToXY(self.A,B[0])
        [x1,y1]=map.gpsToXY(self.A,B[1])
        [x,y]=[(x0+x1)/2, (y0+y1)/2]
        self.Bm=map.xyToGPS(self.A,[x,y])
        self.Bm=map.sexagesimauxToDecimaux2(self.Bm)
        #self.Bm=[(B[0][0]+B[1][0])/2, (B[0][1]+B[1][1])/2]  #centre de la porte

        self.listDistance=None       #listDistance[i]=distance en projection sur x1 du iem waypoints i=0 -> A, /!\ le dernier wayoints n'est pas dans la liste
        self.BestCout=[]
        self.meanCout=[]
        
        self.map=[]
        self.H=None
        self.pas=None
        
        self.setNbWaypoint()   #nb de waypoint générer pour tracer la route      
        self.setMap(1852, 1)
        
        self.stopGa=stopGa
        self.isRun=True
        
        self.batterieBestCout=[]
        self.methodeCout=2
        self.tempsBestCout=[]
    
        self.mCout=None
        self.mEvol=None
        self.mChoix=None
        
    def gen(self,nbCellules:int=None, nbGenerations:int=None, mEvol:int=None, mChoix:int=None, mCout:int=None):
        #self.setNbWaypoint()   #nb de waypoint générer pour tracer la route                
        if(self.nbCellules!=None):
            self.nbCellules=nbCellules
        if(self.nbCellules!=None):
            self.nbGenerations=nbGenerations
        if(self.mEvol!=None):
            self.mEvol=mEvol
        if(self.mChoix!=None):
            self.mChoix=mChoix
        if(self.mCout!=None):
            self.mCout=mCout
            
        self.generation=np.zeros((self.nbwaypoints+1,self.nbCellules)) #on travaille en 1D dans le repère de la route le dernier élément est le cout de la cellule
        #self.map=map.Map(self.nbwaypoints, max(2*int(self.largeurRoute),int(math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2)))), 3*24)
        #################
        # Initilisation #
        #################
        
        for k in range(self.nbCellules):                               #on crée les premières cellules                                
            for i in range(0,self.nbwaypoints-1):
                self.generation[i,k]=random.random()*2*self.largeurRoute-self.largeurRoute    #tire la 1er génération
                #self.generation[i,k]=0
            [x,y]=map.gpsToXY(self.B[0],self.B[1])
            largeurporte=math.sqrt(x**2+y**2)
            self.generation[self.nbwaypoints-1,k]=random.random()*largeurporte-largeurporte/2
            #le dernier waypoint
            
            self.fctCout(k,self.methodeCout) #la dernière case est le cout    

        element = lambda T: T[0]
        T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
        T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
        self.BestCout.append(T[0][0])
        self.meanCout.append(statistics.mean([T[i][0] for i in range(len(T))]))
        
        for g in range(self.nbGenerations-1):
            if(self.mEvol==1):
                #####################
                # reproduction      #
                #####################
                self.reproduction(1, self.mChoix) #croissement cellulaire
                self.reproduction(2) #mutation
            elif(self.mEvol==2):
                #############
                # Evolution # 
                #############
                c=self.choixCellules(self.nbCellules//2+1,self.mChoix)
                #on garde que les cellules choisi, les autres sont copier (ou reproduite ?)
                for j in range(self.nbCellules):
                    if(not j in c):
                        self.generation[:,j]=self.generation[:,random.choices(c)[0]]
                
                self.evolution(2)  #évolution avec une certaine méthode
                self.reproduction(2) #mutation
            
            elif(self.mEvol==3):
                #####################
                # reproduction      #
                #####################
                #les enfants sont les cellules qu'on garde pas 
                choix=self.choixCellules(self.nbCellules//3+1,self.mChoix)
                pc=0.1 #proba de corssover
                co=2 #nb de points de crossover
                #croissement génétique
                #on prend (n-k)//2 couple qui font 2 enfants, si k est impaire la cellule est gardé 
                couples=[]
                while len(choix)>2:
                    c=random.choices(choix,k=1)
                    choix.remove(c[0])
                    d=random.choices(choix,k=1)
                    choix.remove(d[0])
                    couples.append([c[0], d[0]])

                nonChoix=[]
                for i in range(self.nbCellules):
                    if(not i in choix):
                        nonChoix.append(i)
                        
                aleatoire=random.choices(nonChoix, k=self.nbCellules//10+1)
                
                if(couples!=[]):
                    for j in nonChoix:
                            #on calcul les points de crossover : on inverse avant et après les points (cf source 1 p17)
                            C=random.choice(couples)
                            prs=0
                            for e in range(co):
                                t=random.sample([i for i in range(self.nbwaypoints-1)], co)
                                t.sort()
                                t.append(self.nbwaypoints)
                                for k in range(co-1):
                                    if(random.random()>pc): #proba que les waypoints s'inversent
                                        e=random.randint(0,1)
                                        for i in range(t[k], t[k+1]):                                        
                                            self.generation[i, j]=self.generation[i, C[e]]
                for j in aleatoire:
                    for i in range(self.nbwaypoints-1):
                        self.generation[i, j]=random.random()*2*self.largeurRoute-self.largeurRoute
                    self.generation[self.nbwaypoints-1,j]=random.random()*map.distanceGPS(self.B[0], self.B[1])-map.distanceGPS(self.B[0], self.B[1])/2#random.random()*math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))-math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))/2 
                
                self.reproduction(2) #mutation 

                
            #calcul du cout de chaque cellules
            for j in range(self.nbCellules): 
                self.fctCout(j,self.methodeCout) 


            element = lambda T: T[0]
            T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
            T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
            self.BestCout.append(T[0][0])
            if(self.methodeCout==2):
                c=self.fctCout(T[0][1],2,True)
                self.batterieBestCout.append(c[0]*100)
                self.tempsBestCout.append(c[1])
            self.meanCout.append(statistics.mean([T[i][0] for i in range(len(T))]))


            if(self.stopGa.verrou):
                print("fin gen : externe")
                self.isRun=False
                break
        
        self.isRun=False
    
    def run(self):
        self.gen(self.nbCellules, self.nbGenerations, self.mEvol, self.mChoix, self.mCout) #evol, choix
    
    def setRun(self,nbCellules:int, nbGenerations:int, mEvol:int, mChoix:int, mCout:int):
        self.nbCellules=nbCellules
        self.nbGenerations=nbGenerations
        self.mEvol=mEvol
        self.mChoix=mChoix
        self.mCout=self.mCout
        
    def setMap(self, pas2D:float, time:int):
        self.pas=pas2D
        self.H=time
        
        #la carte est adapté au ligne de waypoints
        #chaque colonne de la map est un segment de waypoints
        self.map=[[map.Case(self.R1ToR0(j, i), self.H) for j in range(-int(self.largeurRoute//self.pas), int(self.largeurRoute//self.pas)+1)] for i in range(self.nbwaypoints-1)]
        distanceB1B2=map.distanceGPS(self.B[0],self.B[1])
        self.map.append([map.Case(self.R1ToR0(j, self.nbwaypoints), self.H) for j in range(-int(distanceB1B2/2//self.pas), int(distanceB1B2/2//self.pas))])
        
    def R1ToMap(self, d:float, r:int):
        r=[r, int(d//self.pas+self.largeurRoute//self.pas)]
        if(0<=r[0]< len(self.map)):
            if(not 0<=r[1]<len(self.map[r[0]])):
                
                return r
        else:
            
            return r
        return r
    
    def vent(self, d:float, r:int, h:int):
        [i,j]=self.R1ToMap(d,r)
        if(0<=i<=self.nbwaypoints):
            if(0<=j<len(self.map[i])):
                return self.map[i][j].vent(h)
    
    def uv(self, d:float, r:int, h:int):
        [i,j]=self.R1ToMap(d,r)
        if(0<=i<=self.nbwaypoints):
            if(0<=j<len(self.map[i])):
                return self.map[i][j].uv(h)
    
    def setNbWaypoint(self):
        """Cela permet de set automatiquement le nb de waypoint. La distance en projection sur x1 entre 
        deux waypoints est une fonction croissante (type ln)
        Le dernier waypoint est sur l'axe B[0], B[1] donc la distance entre l'avant dernier waypoint et le suivant est variable suivant la cellule
        
        Il y a donc au moins un waypoint : celui sur l'axe B[0], B[1]"""
        a=0.025*1852
        b=0.5*1852
        c=1852 #le premier point est à 1 mile nautique
        self.listDistance=[c]
        distanceAB=map.distanceGPS(self.A,self.Bm, 2)

        i=1
        while(self.listDistance[-1]<distanceAB):
            self.listDistance.append(self.listDistance[-1]+a*i**2+b*i+c)
            #self.listDistance.append(self.listDistance[-1]+math.log(a*i**2+b*i+c)+c)
            i+=1
        self.nbwaypoints=i
        
        return True
        
    def R1ToR0(self, r:float, d:int, gps=True)->list:
        """R1 : repère de la route
        R0 : repère terrestre
        r : largeur par rapport a la route
        d : indice de la perpendiculaire"""
        if(d<self.nbwaypoints-1): #les premiers points
            [x,y]=map.gpsToXY(self.A,self.Bm)
            alpha=math.atan2(y,x) 
            gama=math.atan2(r, self.listDistance[d])
            distance=math.sqrt(self.listDistance[d]**2+r**2)
            r=[distance*math.cos(alpha+gama),distance*math.sin(alpha+gama)] #"normal"
            if(gps):
                return map.xyToGPS(self.A, r)
            else:
                return r
        elif(d==self.nbwaypoints-1): # le dernier est sur l'axe B1, B2
            [xb,yb]=map.gpsToXY(self.B[0], self.B[1])
            beta=math.atan2(yb,xb) #azimut B0-B1 angle sur le quel le dernier waypoint se balade
            #r : distance entre Bm et le dernier waypoints dans l'axe de la porte
            x=r*math.cos(beta)
            y=r*math.cos(beta)
            P=map.xyToGPS(self.Bm, [x,y])
            if(gps):
                return P
            else:
                return map.gpsToXY(self.A, P)

    def fctCout(self, k:int, coef:int=2, getInfo:bool=False):
        if(coef==0): #distance
            """k : indice de la cellule"""
            s=0 #longueur du chemin
            p=self.C
            for j in range(self.nbwaypoints):
                w=self.R1ToR0(self.generation[j,k], j, True)
                [x,y]=map.gpsToXY(p,w)
                s+=math.sqrt(x**2+y**2)
                p=w
            self.generation[self.nbwaypoints, k]=s
        
        elif(coef==1):
            #on prend la vitesse du vent au premier waypoint A et on prend la direction entre A et B
            a=[self.generation[0,k], 0]
            temps=0   #en h
            for i in range(1, self.nbwaypoints): 
                b=[self.generation[i,k], i]
                ###distance AB
                A=self.R1ToR0(a[0], a[1], True)
                B=self.R1ToR0(b[0], b[1], True)
                distanceAB=map.distanceGPS(A,B)
                ##vitesse AB
                #vent reel AB    
                [Vspd, Vdir]=self.vent(a[0], a[1], int(temps))

                #vent apparent 
                #on suppose que seul Vdir est impacté 
                [x,y]=map.gpsToXY(A,B)                          #on génère les x,y de A p/r à B
                Rv=math.atan2(x, y)*180/math.pi            #cap de A à B
                if(Rv<0):
                    Rv+=360
                VAdir=Vdir-Rv
                if(VAdir<-180):
                    VAdir+=360
                if(VAdir>180):
                    VAdir-=360
                
                #vitesse bateau surface :
                Vsuface=g(Vspd, VAdir)

                if(Vsuface<=0):
                    t=1000+2*temps
                else:
                    t=(distanceAB/1852)/Vsuface
                temps+=t
                a=b
            self.generation[self.nbwaypoints, k]=temps

        elif(coef==2):

            a=[self.generation[0,k], 0]
            temps=0   #en h
            energie=0 #différence production/conso en W 
            
            batterieTot=1000
            batterie=batterieTot*0.7
            resultat=0
            for i in range(1, self.nbwaypoints): 
                b=[self.generation[i,k], i]
                ###distance AB
                #print("dans cout : a", a, "b", b) 
                A=self.R1ToR0(a[0], a[1], True)
                B=self.R1ToR0(b[0], b[1], True)
                distanceAB=map.distanceGPS(A,B)
                ##vitesse AB
                #vent reel AB    
                [Vspd, Vdir]=self.vent(a[0], a[1], int(temps))
                #vent apparent 
                #on suppose que seul Vdir est impacté 
                [x,y]=map.gpsToXY(A,B)                          #on génère les x,y de A p/r à B
                Rv=math.atan2(x, y)*180/math.pi            #cap de A à B

                VAdir=Vdir-Rv
                if(VAdir<-180):
                    VAdir+=360
                if(VAdir>180):
                    VAdir-=360
                #vitesse bateau surface :
                Vsurface=g(Vspd, VAdir)
                
                if(Vsurface<=0):
                    t=1000+2*temps
                else:
                    t=(distanceAB/1852)/Vsurface

                uv=self.uv(a[0], a[1],int(temps))
                #energie
                [conso, prod]=e(Vspd, uv) #en W

                energie+=prod-conso
                batterie+=prod-conso
                
                if(batterie>batterieTot):
                    batterie=batterieTot
                if(batterie<0):
                    batterie=0
                    resultat=abs(2*resultat)+1000
                    t=1000
                if(batterie/batterieTot<0.1):
                    t*=3

                temps+=t
                
                a=b

                
                resultat+=(prod*(1-batterie/batterieTot)+conso**3/(1+batterie/batterieTot)+1)*t

            if(getInfo):
                return [batterie/batterieTot, temps]
            else:
                self.generation[self.nbwaypoints, k]=resultat
            
    def choixCellules(self, k:int, m:int)->list:
        """choisi les numéros des k cellules à garder 
        en utilisant la methode m:
        1 : Sélection par rang (on prend les k meilleurs)
        2 : Probabilité de sélection proportionnelle à l'adaptation (on en prend k aléatoirement prépondérant a sa fct cout)
        3 : Sélection par tournoi 1vs1 jusqu'a ce qu'il en reste k
        4 : Sélection uniforme
        """
        T=[self.generation[self.nbwaypoints,i] for i in range(self.nbCellules)] #liste des couts
        
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
            retour=[]
            proba=0.7
            while len(retour)<k:            #complexite nbCellule-k
                t=random.choices(indice,k=2) #prend 2 cellules
                if(T[t[0]]<T[t[1]] and random.random()<proba): #regarde la plus forte (forte=cout plus petit) avec une proba >0.5
                    retour.append(t[0])    #la plus forte reste 
                else:
                    retour.append(t[1])
            return retour

        else:  
            return random.choices([i for i in range(self.nbCellules)],k=k) #choix alléatoire
    
    def evolution(self,m:int):
        """igen : numéro de la génération en cours
        m : méthode d'évolution
        1: translation aléatoire
        2: fusion cellulaire
        """
        coef=0.1
        if(m==1): #on deplace chaque point de [-coef; coef]
            for i in range(self.nbCellules):
                for j in range(self.nbwaypoints):
                    self.generation[j, i]+=random.random()*2*coef-coef      #essayer avec la méthode du recuit simulé 
        
        elif(m==2): #fusion cellulaire : on prend deux cellules et on mixe certaine cellules dans les deux cellules
            probaFusionWaypoint=50/100  #proba de fusion
            for i in range(0,self.nbCellules,2):
                for j in range(self.nbwaypoints):
                    if(probaFusionWaypoint>random.random()):
                        self.generation[j, i+1]=(self.generation[j,i]+self.generation[j,i+1])/2 #moyenne des waypoints
                        
    def reproduction(self, m:int, k:int=0):
        """Avec un départ de n cellules, on en a sélectionné k donc on complètent les n-k cellules manquante
        on prend la liste des indices des cellules qu'on garde et m la méthode de reproduction"""
        if(m==1):
            indice=self.choixCellules(self.nbCellules//2+1,k)
            pc=0.5 #proba de corssover
            co=self.nbwaypoints//10+1 #nb de points de crossover
            #croissement génétique
            #on prend (n-k)//2 couple qui font 2 enfants, si k est impaire la cellule est gardé 
            couples=[]
            while len(indice)>2:
                c=random.choices(indice,k=1)
                indice.remove(c[0])
                d=random.choices(indice,k=1)
                indice.remove(d[0])
                couples.append([c[0], d[0]])

                
            for C in couples:
                #on calcul les points de crossover : on inverse avant et après les points (cf source 1 p17)
                #prs=0
                for e in range(co):
                    t=random.sample([i for i in range(self.nbwaypoints-1)], co)
                    t.sort()
                    t.append(self.nbwaypoints)
                    for k in range(co-1):
                        if(random.random()>pc): #proba que les waypoints s'inversent
                            for i in range(t[k], t[k+1]):
                                self.generation[i, C[0]],self.generation[i, C[1]]=self.generation[i, C[1]],self.generation[i, C[0]]
        
        elif(m==2):
            ##mutation
            pm=0.1
            coef=1852/1000 #coef de mutation
            for j in range(self.nbCellules):
                for i in range(self.nbwaypoints):
                    if(pm>random.random()):
                        self.generation[i,j]+=random.random()*coef*self.generation[i,j]-coef*self.generation[i,j]/2 # we
                        
                        #on vérifie qu'on sort pas de la route
                        if(self.generation[i,j]>self.largeurRoute):
                            self.generation[i,j]=self.largeurRoute
                        elif(self.generation[i,j]<-self.largeurRoute):
                            self.generation[i,j]=-self.largeurRoute
            

    def resultat(self, gps=True):
        element = lambda T: T[0]
        T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
        T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
        r=[self.generation[j,T[0][1]] for j in range(self.nbwaypoints)]
        if(gps):
            return self.R1ToR0List(r,gps)
        else:
            return r
    
    def R1ToR0List(self, list:list, gps:bool=False)->list:
        r=[]
        for i in range(len(list)):
            r.append(self.R1ToR0(list[i],i,gps))
        return r
    
    def plot(self, show:bool=True):
        plt.figure(1)
        plt.subplot(211)
        #cout en m (optimisation distance)
        plt.plot([i for i in range(len(self.BestCout))], [e for e in self.BestCout], "r")
        plt.plot([i for i in range(len(self.meanCout))], [e for e in self.meanCout], "b")

        plt.title("évolution du cout")
        plt.legend(("best", "mean"))
        plt.xlabel("générations")
        plt.ylabel("cout")
        plt.ylim(min(self.BestCout), max(self.BestCout))
        
        plt.subplot(212)
        plt.plot([i for i in range(len(self.BestCout))], [e for e in self.BestCout], "r")
        plt.plot([i for i in range(len(self.meanCout))], [e for e in self.meanCout], "b")

        plt.title("évolution du cout" )
        plt.legend(("best", "mean"))
        plt.xlabel("générations")
        plt.ylabel("cout")
        

        if(self.methodeCout==2):
            plt.figure(2)
            plt.subplot(211)
            plt.plot([i for i in range(len(self.batterieBestCout))],self.batterieBestCout)
            plt.xlabel("Générations")
            plt.ylabel("% batterie")
            plt.title("%  batterie restante de la meilleur cellule de chaque génération")
            plt.subplot(212)
            
            plt.plot([i for i in range(len(self.tempsBestCout))],self.tempsBestCout)
            plt.xlabel("Générations")
            plt.ylabel("cout (temps)")
            plt.title("cout en temps de la meilleur cellule de chaque génération")
            plt.subplot(212)
        if(show):
            plt.show()
            
    
    def save(self, nomFichier:str="map"):
        print("saving")
        #self.A=map.sexagesimauxToDecimaux2(self.A)
        #self.Bm=map.sexagesimauxToDecimaux2(self.Bm)
        #self.B[0]=map.sexagesimauxToDecimaux2(self.B[0])
        #self.B[1]=map.sexagesimauxToDecimaux2(self.B[1])
        carte = folium.Map(location=self.A, tiles='OpenStreetMap', zoom_start=10)
        
        #trace le fond
        folium.Marker(location=self.A, popup = "Depart Theorique", icon=folium.Icon(color='red')).add_to(carte)
        folium.Marker(location=self.C, popup="position bateau", icon=folium.Icon(color='green')).add_to(carte)
        folium.Marker(location=self.Bm, popup="centre porte", icon=folium.Icon(color='blue')).add_to(carte)
        folium.PolyLine(self.B, color="blue", weight=2.5, opacity=1).add_to(carte)
        folium.PolyLine([self.A,self.Bm], color="yellow", weight=2.5, opacity=1).add_to(carte)
        
        C1=map.sexagesimauxToDecimaux2(self.R1ToR0(self.largeurRoute, 0, True))
        C2=map.sexagesimauxToDecimaux2(self.R1ToR0(-self.largeurRoute, 0, True))
        C3=map.sexagesimauxToDecimaux2(self.R1ToR0(self.largeurRoute, self.nbwaypoints-2, True))
        C4=map.sexagesimauxToDecimaux2(self.R1ToR0(-self.largeurRoute, self.nbwaypoints-2, True))
        folium.PolyLine([C1,C3], color="green", weight=2.5, opacity=1).add_to(carte)
        folium.PolyLine([C2,C4], color="green", weight=2.5, opacity=1).add_to(carte)
        
        #trace les paralleles : 
        for i in range(self.nbwaypoints):
            D1=map.sexagesimauxToDecimaux2(self.R1ToR0(self.largeurRoute, i, True))
            D2=map.sexagesimauxToDecimaux2(self.R1ToR0(-self.largeurRoute, i, True))
            folium.PolyLine([D1,D2], color="yellow", weight=2.5, opacity=1).add_to(carte)
        
        #resultat 
        folium.PolyLine([self.C]+self.resultat(True), color="red", weight=2.5, opacity=1).add_to(carte)

        carte.save(outfile=nomFichier+'.html')
        print("finish")

if __name__ == "__main__":
    A=[[0,0,0,"N"],[10,0,0,"W"]]
    porte=[[[1,1,0,"N"],[5,0,0,"E"]],[[1,1,0,"S"],[5,0,0,"E"]]]

    stGa=StopGA(None,None)
    ga=Ga(A, A, porte, 50*1852, stGa)
    ga.setRun(20, 20, 3, 1, 2)
    
    stGa.ga=ga

    stGa.start()
    ga.start()
    
    ga.join()
    stGa.join()

    ga.save()
    ga.plot()

