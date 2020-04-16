import numpy as np
import random
from sklearn.cluster import KMeans
import hdbscan
import matplotlib.pyplot as plt
import math
from sklearn.cluster import KMeans
import statistics
import time
import sys 
import json
import requests 

def iN(A, T):
    if(T[1][0]>=A[0]>=T[0][0] and T[1][1]>=A[1]>=T[0][1]):
        return True
    else:
        return False

def sexagesimauxToDecimaux(A:list, rad:bool=False)->float:
    """A[0]°A[1]'A[2]''.."""
    if(isSexagesimaux(A)):
        r=0
        for i in range(0,len(A)-1):
            r+=A[i]*1/(60**i)
        if(A[-1]=='S' or A[-1]=='W' or A[-1]=='O'):
            r=-r
        if(not rad):
            return r
        else:
            return r*math.pi/180
    else: #si on est en décimal, on est en deg
        if(rad):
            return A*math.pi/160
        else:
            return A
    
def sexagesimauxToDecimaux2(A:list, rad:bool=False)->list:
    """A: lat/long"""
    return [sexagesimauxToDecimaux(A[0], rad), sexagesimauxToDecimaux(A[1],rad)]

def distanceGPS(A:list, B:list, methode:int=3,unite:str="m")->float:
    #méthode des sinus http://villemin.gerard.free.fr/aGeograp/Distance.htm
    ##forcer a repasser en sexa pour éviter le cas ou on est en decimaux et on doit passer en radiant
    if(methode==1):
        A=sexagesimauxToDecimaux2(A, True)
        B=sexagesimauxToDecimaux2(B, True)
        distance=math.acos(math.sin(A[0])*math.sin(B[0])+math.cos(A[0])*math.cos(B[0])*math.cos(B[1]-A[1]))*6378137
    #métode de pythagore :
    elif(methode==2):
        A=sexagesimauxToDecimaux2(A, False)
        B=sexagesimauxToDecimaux2(B, False)
        [x,y]=gpsToXY(A,B) #A,B en decimaux deg
        distance=math.sqrt(x**2+y**2)
    #méthode des Haversine 
    else:
        A=sexagesimauxToDecimaux2(A, True)
        B=sexagesimauxToDecimaux2(B, True)
        a=math.sin(B[0]-A[0])**2+math.cos(A[0])*math.cos(B[0])*math.sin(B[0]-A[0])**2
        distance=6378137*math.atan(math.sqrt(a)/math.sqrt(1-a))
        if(distance==0):
            distance=distanceGPS(decimauxToSexagesimaux2(A, True), decimauxToSexagesimaux2(B, True), 2, "m")
    if(unite.lower()=="m"):
        return distance
    if(unite.lower()=="nm" or unite.lower()=="kn" or unite.lower()=="kns"):
        return distance/1852
    if(unite.lower()=="km"):
        return distance/1000
    
def decimauxToSexagesimaux(x:float,l:str, rad:bool=False)->list:
    """rad c'est si cela provient d'une distance en rad et non deg"""
    if(isDecimaux(x)):
        if(rad):
            x=180.0*x/math.pi
        A=[]
        y,x=x,abs(x)
        for i in range(2):
            A.append(int(x))
            x=(x-int(x))*60
        A.append(x)
        if((l=='longitude' or  l=='long') and y<0):
            A.append('W')
            #A.append('O')
        elif((l=='longitude' or  l=='long') and y>=0):
            A.append('E')
        elif((l=='latitude' or l=='lat') and y<0):
            A.append('S')
        elif((l=='latitude' or l=='lat') and y>=0):
            A.append('N')
        #print("avant",A)
        
        #if(A[2]<0):
        #    A[2]=60+A[2]
        #    if(A[1]<=0):
        #        A[1]-=1
        #    else:
        #        A[1]+=1
        #if(A[1]<0):
        #    A[1]=60+A[1]
        #    if(A[0]<=0):
        #        A[0]-=1
        #    else:
        #        A[0]+=1
        #if(A[0]<0):
        #    A[0]=abs(A[0])
        #    if(A[-1]=='W' or A[-1]=='O'):
        #        A[-1]='E'
        #    elif(A[-1]=='S'):
        #        A[-1]='N'
        #    elif(A[-1]=='E'):
        #        A[-1]='W'
        #    else:
        #        A[-1]='S'
        #print("après",A)
        return A
    else:
        return x
    
def decimauxToSexagesimaux2(X:list, rad:bool=False)->list:
    """X [lat,long]"""
    if(isDecimaux2(X)):
        return [decimauxToSexagesimaux(X[0], "lat", rad), decimauxToSexagesimaux(X[1], "long", rad)]
    else:
        return X

def isDecimaux(gps)->bool:
    return not type(gps)==type([])
def isSexagesimaux(gps)->bool:
    return not isDecimaux(gps)
def isDecimaux2(gps)->bool:
    return isDecimaux(gps[0])
def isSexagesimaux2(gps):
    return not isDecimaux2(gps)

def gpsToXY(A:list, B:list, unite:str="m")->list:
    """A=[lat,long] B=[lat,long]"""
    A=sexagesimauxToDecimaux2(A)
    B=sexagesimauxToDecimaux2(B)
            
    x=(B[1]-A[1])*math.cos((A[0]+B[0])/2*math.pi/180)
    y=B[0]-A[0]
    #return[x*60*1852,y*60*1852] #1min d'arc=1milles marin=1852m  http://villemin.gerard.free.fr/aGeograp/Distance.htm
    if(unite.lower()=="m"):
        return [x*60*1852,y*60*1852]
    if(unite.lower()=="nm" or unite.lower()=="kn" or unite.lower()=="kns"):
        return [x*60,y*60]
    if(unite.lower()=="km"):
        return [x*60*1.852,y*60*1.852]

def xyToGPS(zero:list,X:list, dec=True)->list: ##possible que x et y soit inversé
    """Zero est en co GPS lat/long"""
    P=[0,0]
    zero=sexagesimauxToDecimaux2(zero)
    #X=sexagesimauxToDecimaux2(X)
    X=[X[0]/(60*1852), X[1]/(60*1852)]
    P[0]=zero[0]+X[1]
    c=math.cos((zero[0]+P[0])/2*math.pi/180)
    if(c!=0):
        P[1]=zero[1]+X[0]/c
    else: 
        #on utilise la méthode des sinus http://villemin.gerard.free.fr/aGeograp/Distance.htm
        #on suppose que les deux distance sont égale:
        d=math.sqrt(X[0]**2+X[1]**2)
        a=math.acos(math.cos(d/6378137)-math.sin(zero[0]*math.pi/180)*math.sin(P[0]*math.pi/180))
        if(math.cos(zero[0]*math.pi/180)*math.cos(P[0]*math.pi/180)!=0):
            P[1]=a/(math.cos(zero[0]*math.pi/180)*math.cos(P[0]*math.pi/180))
        else :
            print("error xyToGPS")
        
    if(dec): #si on veut le résulat en decimal ou en sexa
        return P
    else:
        return decimauxToSexagesimaux2(P)

class Map:
    def __init__(self, zero:list, A:list, pas:float, ptemps:int):
        """zero origine en lat/long, A point extrème lat/long, 
        ptemps est le nombre de translation dans le temps. Le pas est une heure"""
        [x,y]=gpsToXY(zero,A)
        self.x=y
        self.y=x
        self.pas=pas
        self.n=abs(int(x/pas))
        self.m=abs(int(y/pas))
        self.ptemps=ptemps
        #changement d'origine
        if(x<0 and y>0):
            zero=[zero[0], A[1]]
        elif(x>0 and y<0):
            zero=[A[0], zero[1]]
        elif(x<0 and y<0):
            zero=A
                                        #+1 car ptemps=0 -> pas de prévision
        self.map=np.zeros((self.n,self.m,ptemps+1,12)) #profondeur, vitesse vent (v,d), courant (c,d), houle (A,f,d), Tair, Hair, Teau, Salinité eau
        
        #en latitude/longitude
        if(type(zero[0])==type([])): #de type deg min sec 
            zero[0]=sexagesimauxToDecimaux(zero[0])
            zero[1]=sexagesimauxToDecimaux(zero[1])
        self.zero=zero
        
    def R0ToMap(self,P:list)->list:
        """P: [lat,long]"""
        [x,y]=gpsToXY(self.zero,P)
        i=int(x/self.pas)
        j=int(y/self.pas)
        if(i>=0 and j>=0):
            return [i,j]
        else:
            p=decimauxToSexagesimaux2(P)
            #print("Hors Map :","P:",p,"x,y",[x,y],"i,j",[i,j])
            self.agrandissement(P)
            return self.R0ToMap(P)
            #return None
    
    def MapToR0(self, i:int, j:int)->list:
        [x,y]=self.MapsToXY(i,j)
        return xyToGPS(self.zero, [x,y])
   
    def MapToXY(self,i:int, j:int, unite:str="m")->list:
        x=i*self.pas
        y=j*self.pas
        if(unite.lower()=="m"):
            return [x,y]
        if(unite.lower()=="nm" or unite.lower()=="kn" or unite.lower()=="kns"):
            return [x/1852,y/1852]
        if(unite.lower()=="km"):
            return [x/1000,y/1000]
    
    def profondeur(self, i,j,h): #peut dépendre de la marée ? 
        #if h<currenttime-T0  -> setdata h et décale le reste
        if(h>self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps
        if(self.map[i,j,h,0]==0):
            self.setData(i,j,h)
        return self.map[i,j,h,0] #profondeur en m >0, si p<0 -> sol 
    
    def vent(self, i,j,h):
        #print(i,j,h, self.n, self.m, self.ptemps)
        if(h>=self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps-1
        #if h<currenttime-T0 #setData
        if(self.map[i,j,h,1]==0):
            self.setData(i,j,h)
        return [self.map[i,j,h,1], self.map[i,j,h,2]] #vent spd, dir
    
    def courant(self, i,j,h):
        if(h>self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps
        #if h<currenttime-T0 #setData
        if(self.map[i,j,h,3]==0):
            self.setData(i,j,h)
        return [self.map[i,j,h,3], self.map[i,j,h,4]] #courant spd dir
    
    def houle(self, i,j,h):
        if(h>self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps
        #if h<currenttime-T0 #setData
        if(self.map[i,j,h,5]==0):
            self.setData(i,j,h)
        return [self.map[i,j,h,5], self.map[i,j,h,6], self.map[i,j,7]]  #A,f, dir     
    
    def air(self, i,j,h):
        if(h>self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps
        #if h<currenttime-T0 #setData
        if(self.map[i,j,h,6]==0):
            self.setData(i,j,h)
        return [self.map[i,j,h,8], self.map[i,j,h,9]] #T, H
    
    def eau(self,i,j,h):
        if(h>self.ptemps): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.ptemps
        #if h<currenttime-T0 #setData
        if(self.map[i,j,h,7]==0):
            self.setData(i,j,h)
        return [self.map[i,j,h,10], self.map[i,j,h,11]] #T, S
    
    def setData(self,i,j,h)->None:
        #print("setData: ",i,j,h)
        #un truc [lat,long]=self.MapToR0(i,j)
        self.map[i,j,h,0]=random.random()*2-1+10      #profondeur
        self.map[i,j,h,1]=random.random()*5+10     #vent spd
        self.map[i,j,h,2]=random.random()*10-5+180        #vent dir
        self.map[i,j,h,3]=random.random()*2-1+3     #courant spd
        self.map[i,j,h,4]=random.random()*4-2+90     #courant dir
        self.map[i,j,h,5]=random.random()*2-1+2     #houle A
        self.map[i,j,h,6]=random.random()*2+1     #houle freq
        self.map[i,j,h,7]=random.random()*5+90     #houle dir
        self.map[i,j,h,8]=20     #T air
        self.map[i,j,h,9]=50     #H air
        self.map[i,j,h,10]=12    #T eau
        self.map[i,j,h,11]=34    #S eau
        return None
    
    def agrandissement(self, A:list)->None: #a vérifier
        """on agrandi la carte jusqua ce que A soit dans la map"""
        #print("starting agrandissement")
        t0=time.time()
        [x,y]=gpsToXY(self.zero,A)
        [i,j]=[int(x/self.pas), int(y/self.pas)]
        if(0<=i<=self.n and 0<=j<=self.m): #pas besoin de grandir
            #print("0")
            return None
        
        elif(i>self.n or j>self.m):
            #print("1")
            #si on a pas besoin de changer l'origine
            newmap=np.zeros((max(self.n,i), max(self.m,j), self.ptemps,12))
            for l in range(min(self.n,i)):
                for k in range(min(self.m,j)):
                    for t in range(self.ptemps):
                        for m in range(12):
                            newmap[l,k,t,m]=self.map[l,k,t,m]
            self.map=newmap
            self.n=max(self.n,i)
            self.m=max(self.m,j)
        
        #si on a besoin de changer l'origine
        elif(i<0 and j>=0):
            #print("2")
            #on rajoute des cases vers le bas
            newmap=np.zeros((self.n+abs(i), self.m, self.ptemps,12))
            for l in range(self.n):
                #print(l)
                for k in range(self.m):
                    for t in range(self.ptemps):
                        for m in range(12):
                            newmap[l+abs(i),k,t,m]=self.map[l,k,t,m]
            self.n=self.n+abs(i)
            self.map=newmap
            self.zero=[self.zero[0], A[1]]
            
        elif(i>=0 and j<0):
            #print("3")
            newmap=np.zeros((self.n, self.m+abs(j), self.ptemps,12))
            for l in range(self.n):
                for k in range(self.m):
                    for t in range(self.ptemps):
                        for m in range(12):
                            newmap[l,k+abs(j),t,m]=self.map[l,k,t,m]
            self.m=self.m+abs(j)
            self.map=newmap
            self.zero=[A[0], self.zero[1]]
        
        elif(i<0 and j<0):
            #print("4")
            newmap=np.zeros((self.n+abs(i), self.m+abs(j), self.ptemps,12))
            for l in range(self.n):
                for k in range(self.m):
                    for t in range(self.ptemps):
                        for m in range(12):
                            newmap[l+abs(i),k+abs(j),t,m]=self.map[l,k,t,m]
            self.n=self.n+abs(i)
            self.m=self.m+abs(j)
            self.map=newmap
            self.zero=A
        else :
            #print("error map")
            return "error"
        #print("finishing agrandissement in ", time.time()-t0, "s")
   
    def supprime(self,P:list): #a vérifier
        [i,j]=self.ROtoMap(P)
        if(i<0):
            i=self.n
        if(j<0):
            j=self.m
        newmap=np.zeros((min(self.n,i), min(self.m,j), self.ptemps,12))
        for l in range(min(self.n,i)):
                for k in range(min(self.m,j)):
                    for t in range(self.ptemps):
                        for m in range(12):
                            newmap[l,k,t,m]=self.map[l,k,t,m]
        self.map=newmap
        self.n=i
        self.m=j
        
class Map2:
    def __init__(self, zero:list, A:list, pas:float, H:int):
        [x,y]=gpsToXY(zero,A)
        self.x=y
        self.y=x
        self.pas=pas
        self.n=abs(int(x/pas))+1
        self.m=abs(int(y/pas))+1
        self.H=H
        
        #changement d'origine
        if(x<0 and y>0):
            zero,A=[zero[0], A[1]],[A[0], zero[1]]
        elif(x>0 and y<0):
            zero,A=[A[0], zero[1]],[zero[0], A[1]]
        elif(x<0 and y<0):
            zero,A=A,zero
        #en latitude/longitude
        self.zero=sexagesimauxToDecimaux2(zero)
        self.A=sexagesimauxToDecimaux2(A)
        
        ##génération des cases 
        self.map=[]
        for i in range(self.n):
            y=[]
            for j in range(self.m):
                y.append(Case(self.MapToR0(i,j), self.H))
            self.map.append(y)
        
        
        #compteur d'agrandisement
        
    def R0ToMap(self,P:list, agran:bool=True)->list:
        """P: [lat,long]"""
        [x,y]=gpsToXY(self.zero,P)
        i=int(x/self.pas)
        j=int(y/self.pas)
        if(i>=0 and j>=0 and i<self.n and j<self.m):
            return [i,j]
        else:
            p=decimauxToSexagesimaux2(P)
            #print("Hors Map :","P:",p,"x,y",[x,y],"i,j",[i,j])
            if(agran):
                self.agrandissement(P)
                return self.R0ToMap(P)
            return [i,j]
        
    def MapToR0(self, i:int, j:int)->list:
        [x,y]=self.MapToXY(i,j)
        return xyToGPS(self.zero, [x,y])
   
    def MapToXY(self,i:int, j:int, unite:str="m")->list:
        x=i*self.pas
        y=j*self.pas
        if(unite.lower()=="m"):
            return [x,y]
        if(unite.lower()=="nm" or unite.lower()=="kn" or unite.lower()=="kns"):
            return [x/1852,y/1852]
        if(unite.lower()=="km"):
            return [x/1000,y/1000]

    def agrandissement(self, A:list)->None: #a vérifier
        """on agrandi la carte jusqua ce que A soit dans la map"""
        A=sexagesimauxToDecimaux2(A)
        #print("starting agrandissement")
        t0=time.time()
        
        [x,y]=gpsToXY(self.zero,A)
        i=int(x/self.pas)
        j=int(y/self.pas)
        #[i,j]=self.R0ToMap(A, False) 
        
        [xa,ya]=gpsToXY(self.zero,A)
        [xc,yc]=gpsToXY(self.zero,self.A)
        #print("A", [xa/1852,ya/1852], "self.A", [xc/1852,yc/1852])
        #print("max",[max(xa,xc)/1852,max(ya,yc)/1852], "min",[min(xa,0)/1852,min(ya,0)/1852])
        
        B=xyToGPS(self.zero,[max(xa,xc),max(ya,yc)])
        zero=xyToGPS(self.zero,[min(xa,0),min(ya,0)])

        #print("agrandisement :")
        #print("Avant : zero",decimauxToSexagesimaux2(self.zero),"A" ,decimauxToSexagesimaux2(self.A))
        #print("Apres : zero",decimauxToSexagesimaux2(zero),"A" ,decimauxToSexagesimaux2(B))
        if(0<=i<self.n and 0<=j<self.m): #pas besoin de grandir
            #print("0")
            return None
        
        elif((i>self.n or j>self.m) and (i>=0 and j>=0)):
            #print("1")
            #si on a pas besoin de changer l'origine
        
            ##on augmente en 2 fois : 
            for l in range(min(self.n,i)):
                for k in range(min(self.m,j), max(self.m,j)):
                    self.map[l].append(Case(self.MapToR0(l,k), self.H))
            
            for l in range(min(self.n, j), max(self.m,j)):
                y=[]
                for k in range(max(self.m,j)):
                    y.append(Case(self.MapToR0(l,k), self.H))
                self.map.append(y)
            
            self.n=max(self.n,i)
            self.m=max(self.m,j)
            self.A=B
        
        ####test
        else:
            #print("2")
            #on décale le zéro et les cases
            newMap=Map2(zero,B, self.pas, self.H) #on crée une map plus grande
            p=newMap.n-self.n #on regarde sur quel angle on agrandi (égal à i,j si négatif ??? maybe)
            q=newMap.m-self.m #ne peut pas être strictement négatif
            for l in range(self.n):
                for k in range(self.m):

                    if(self.map[l][k].gen): #si la cellule à été généré
                        newMap.map[l+p][k+q]=self.map[l][k] #on la copie
            self.map=newMap.map #on échange les map
            self.A=newMap.A
            self.zero=newMap.zero
            self.n=newMap.n
            self.m=newMap.m
            self.x=newMap.x
            self.y=newMap.y
        """
        #si on a besoin de changer l'origine
        elif(i<0 and j>=0):
            print("2")
            #on décale les cases vers le bas
            newMap=Map2(zero,B, self.pas, self.H)
            for l in range(self.n):
                for k in range(self.m):
                    if(self.map[l][k].gen): #si la cellule à été généré
                        newMap.map[l+abs(i)][k]=self.map[l][k] #on la copie
            self.map=newMap.map #on échange les map
            self.A=newMap.A
            self.zero=newMap.zero
            self.n=newMap.n
            self.m=newMap.m
            self.x=newMap.x
            self.y=newMap.y
            
        elif(i>=0 and j<0):
            print("3")
            newMap=Map2(zero,B, self.pas, self.H)
            for l in range(self.n):
                for k in range(self.m):
                    if(self.map[l][k].gen): #si la cellule à été généré
                        newMap.map[l][k+abs(j)]=self.map[l][k] #on la copie
            self.map=newMap.map #on échange les map
            self.A=newMap.A
            self.zero=newMap.zero
            self.n=newMap.n
            self.m=newMap.m
            self.x=newMap.x
            self.y=newMap.y

        elif(i<0 and j<0):
            print("4")
            newMap=Map2(zero,B, self.pas, self.H)
            for l in range(self.n):
                for k in range(self.m):
                    if(self.map[l][k].gen): #si la cellule à été généré
                        newMap.map[l+abs(i)][k+abs(j)]=self.map[l][k] #on la copie
            self.map=newMap.map #on échange les map
            self.A=newMap.A
            self.zero=newMap.zero
            self.n=newMap.n
            self.m=newMap.m
            self.x=newMap.x
            self.y=newMap.y
            
        else :
            print("error map")
            return "error"
        """
        #print("finishing agrandissement in ", time.time()-t0, "s")
        

class Map3: ###comme Map2 mais avec un verrou d'écriture sur l'agrandissement, faut-il le mettre sur la lecture ? 
    def __init__(self, zero:list, A:list, pas:float, H:int):
        [x,y]=gpsToXY(zero,A)
        self.x=y
        self.y=x
        self.pas=pas
        self.n=abs(int(x/pas))+1
        self.m=abs(int(y/pas))+1
        self.H=H
        
        #changement d'origine
        if(x<0 and y>0):
            zero,A=[zero[0], A[1]],[A[0], zero[1]]
        elif(x>0 and y<0):
            zero,A=[A[0], zero[1]],[zero[0], A[1]]
        elif(x<0 and y<0):
            zero,A=A,zero
        #en latitude/longitude
        self.zero=sexagesimauxToDecimaux2(zero)
        self.A=sexagesimauxToDecimaux2(A)
        
        ##génération des cases 
        self.map=[]
        for i in range(self.n):
            y=[]
            for j in range(self.m):
                y.append(Case(self.MapToR0(i,j), self.H))
            self.map.append(y)
        
        
        #compteur d'agrandisement
        self.verrou=False
        
    def R0ToMap(self,P:list, agran:bool=True)->list:
        """P: [lat,long]"""
        [x,y]=gpsToXY(self.zero,P)
        i=int(x/self.pas)
        j=int(y/self.pas)
        if(i>=0 and j>=0 and i<self.n and j<self.m):
            return [i,j]
        else:
            p=decimauxToSexagesimaux2(P)
            #print("Hors Map :","P:",p,"x,y",[x,y],"i,j",[i,j])
            if(agran):
                self.agrandissement(P)
                return self.R0ToMap(P)
            return [i,j]
        
    def MapToR0(self, i:int, j:int)->list:
        [x,y]=self.MapToXY(i,j)
        return xyToGPS(self.zero, [x,y])
   
    def MapToXY(self,i:int, j:int, unite:str="m")->list:
        x=i*self.pas
        y=j*self.pas
        if(unite.lower()=="m"):
            return [x,y]
        if(unite.lower()=="nm" or unite.lower()=="kn" or unite.lower()=="kns"):
            return [x/1852,y/1852]
        if(unite.lower()=="km"):
            return [x/1000,y/1000]

    def agrandissement(self, A:list)->None: #a vérifier
        """on agrandi la carte jusqua ce que A soit dans la map"""
        
        if(self.verrou):
            sys.stdout.write("waiting.")
            sys.stdout.flush()
        else:
            sys.stdout.write("prems"+str(decimauxToSexagesimaux2(A))+"\n")
            sys.stdout.flush()
            
        while(self.verrou):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.1) 
        sys.stdout.write("\n")
        sys.stdout.flush()
            
        self.verrou=True    
        
        A=sexagesimauxToDecimaux2(A)
        #print("starting agrandissement")
        t0=time.time()
        
        [x,y]=gpsToXY(self.zero,A)
        i=int(x/self.pas)
        j=int(y/self.pas)
        
        [xa,ya]=gpsToXY(self.zero,A)
        [xc,yc]=gpsToXY(self.zero,self.A)
        
        B=xyToGPS(self.zero,[max(xa,xc),max(ya,yc)])
        zero=xyToGPS(self.zero,[min(xa,0),min(ya,0)])

        if(0<=i<self.n and 0<=j<self.m): #pas besoin de grandir
            #print("0")
            self.verrou=False
            return None
        
        elif((i>self.n or j>self.m) and (i>=0 and j>=0)):
            for l in range(min(self.n,i)):
                for k in range(min(self.m,j), max(self.m,j)):
                    self.map[l].append(Case(self.MapToR0(l,k), self.H))
            
            for l in range(min(self.n, j), max(self.m,j)):
                y=[]
                for k in range(max(self.m,j)):
                    y.append(Case(self.MapToR0(l,k), self.H))
                self.map.append(y)
            
            self.n=max(self.n,i)
            self.m=max(self.m,j)
            self.A=B

        else:
            #on décale le zéro et les cases
            newMap=Map3(zero,B, self.pas, self.H) #on crée une map plus grande
            p=newMap.n-self.n #on regarde sur quel angle on agrandi (égal à i,j si négatif ??? maybe)
            q=newMap.m-self.m #ne peut pas être strictement négatif
            for l in range(self.n):
                for k in range(self.m):
                    #sys.stdout.write("l,k"+ str([l,k])+str([self.n, self.m])+ str([len(self.map), len(self.map[0])])+"\n")
                    #sys.stdout.flush()
                    if(self.map[l][k].gen): #si la cellule à été généré
                        newMap.map[l+p][k+q]=self.map[l][k] #on la copie
            self.map=newMap.map #on échange les map
            self.A=newMap.A
            self.zero=newMap.zero
            self.n=newMap.n
            self.m=newMap.m
            self.x=newMap.x
            self.y=newMap.y

        self.verrou=False

    def vent(self, P:list, h:int, agran:bool=True):
        [i,j]=self.R0ToMap(P, agran)
        if(0<=i<self.n and 0<=j<self.m):
            return self.map[i][j].vent(h)
        else:
            print("error méteo")
            return None
    
    def courant(self, P:list, h:int, agran:bool=True):
        [i,j]=self.R0ToMap(P, agran)
        if(0<=i<self.n and 0<=j<self.m):
            return self.map[i][j].courant(h)
        else:
            print("error méteo")
            return None
    
    def uv(self,P:list, h:int, agran:bool=True):
        [i,j]=self.R0ToMap(P, agran)
        if(0<=i<self.n and 0<=j<self.m):
            return self.map[i][j].uv(h)
        else:
            print("error méteo")
            return None
class Case:
    def __init__(self, coordonnee:list,H:int=3*34):
        self.H=H
        self.content=np.zeros((13,self.H)) #profondeur, vent (spd, dir), courant (spd, dir), houle (A, freq, dir), air (T, H, P) eau (T, S), ciel (UV, nuage)  ?? 
        self.gen=False
        self.coordonnee=coordonnee

    def profondeur(self,h): #peut dépendre de la marée ? 
        #if h<currenttime-T0  -> setdata h et décale le reste
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        if(not self.gen):
            self.setData()
        return self.content[0,h] #profondeur en m >0, si p<0 -> sol 
    
    def vent(self,h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
        return [self.content[1,h], self.content[2,h]] #vent spd, dir
    
    def courant(self,h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
        return [self.content[3,h], self.content[4,h]] #courant spd dir
    
    def houle(self,h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
            
        return [self.content[5,h], self.content[6,h], self.content[7,h]]  #A,f, dir     
    
    def air(self, h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
            
        return [self.content[8,h], self.content[9,h]] #T, H
    
    def eau(self,h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
            
        return [self.content[10,h], self.content[11,h]] #T, S
    
    def uv(self, h):
        if(h>=self.H): #si on a pas les prévisions assez loin, on prend la plus tardive
            h=self.H-1
        #if h<currenttime-T0 #setData
        if(not self.gen):
            self.setData()
        return self.content[12,h]
    
    def setData(self):
        #print("set data", decimauxToSexagesimaux2(self.coordonnee))
        if(False):
            self.coordonnee=sexagesimauxToDecimaux2(self.coordonnee)
            lat=str(self.coordonnee[0])
            lon=str(self.coordonnee[1])
            appid="1603c5460b318182950010668f1ac7da"
            req="https://samples.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid="+appid
            r=requests.get(req)
            j=r.json()
            self.content[0,0]=j["main"]["sea_level"]  #profondeur
            self.content[1,0]=j["wind"]["speed"] #vent spd
            self.content[2,0]=j["wind"]["deg"] #vent deg
            #self.content[3,0]=0         #courant spd
            #self.content[4,0]=0         #courant dir
            self.content[5,0]=random.random()*2-1+2     #houle A
            #self.content[6,h]=random.random()*2+1     #houle freq
            #self.content[7,h]=random.random()*5+90     #houle dir
            self.content[8,0]=273.15-j["main"]["temp_min"]     #T air en C
            self.content[9,0]=j["main"]["humidity"]     #H air
            #self.content[10,h]=12    #T eau
            #self.content[11,h]=34    #S eau
        else:
            for h in range(self.H):
                self.content[0,h]=random.random()*2-1+10      #profondeur
                self.content[1,h]=random.random()*5+10     #vent spd
                self.content[2,h]=random.random()*10-5+180        #vent dir
                self.content[3,h]=random.random()*2-1+3     #courant spd
                self.content[4,h]=random.random()*4-2+90     #courant dir
                self.content[5,h]=random.random()*2-1+2     #houle A
                self.content[6,h]=random.random()*2+1     #houle freq
                self.content[7,h]=random.random()*5+90     #houle dir
                self.content[8,h]=20     #T air
                self.content[9,h]=50     #H air
                self.content[10,h]=12    #T eau
                self.content[11,h]=34    #S eau
                self.content[12,h]=random.randint(6,12)
        self.gen=True
        
class Map4:
    ##le but c'est de faire un map adapté a la Ga
    def __init__(self, zero:list,listDistance:list, largeurRoute:float, pas:float,H:int, porte:list):
        self.listDistance=listDistance
        self.largeurRoute=largeurRoute
        self.pas=pas
        self.zero=zero
        self.porte=porte
        self.porte[0]=map.sexagesimauxToDecimaux2(self.porte[0])
        self.porte[1]=map.sexagesimauxToDecimaux2(self.porte[1])
        
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        [x0,y0]=map.gpsToXY(self.zero,self.porte[0])
        [x1,y1]=map.gpsToXY(self.zero,self.porte[1])
        [x,y]=[(x0+x1)/2, (y0+y1)/2]
        self.Bm=map.xyToGPS(self.zero,[x,y])
        self.Bm=map.sexagesimauxToDecimaux2(self.Bm)
        
        self.H=H
        #generation de la map. 
        self.map=[[Case(self.MapToR0(i,j), H) for j in range(-self.largeurRoute//self.pas,self.largeurRoute//self.pas)] for i in range(len(self.listDistance))]
        self.map.append([Case(self.MapToR0(i,j), H) for j in range(-distanceGPS(-self.porte[0]//(2*self.pas),self.porte[1]//(2*self.pas)))])
    
    def MapToR0(self, i,j):
        """R1 : repère de la route
        R0 : repère terrestre
        i : largeur par rapport a la route
        j : indice de la perpendiculaire"""
        if(i<len(self.listDistance)): #les premiers points
            [x,y]=gpsToXY(self.zero,self.Bm)
            alpha=math.atan2(y,x) 
            gama=math.atan2(j, self.listDistance[i])
            #return [self.listDistance[d]*math.cos(alpha)+r*math.cos(alpha+gama), self.listDistance[d]*math.sin(alpha)+r*math.sin(gama+alpha)]
            distance=math.sqrt(self.listDistance[i]**2+j**2)
            #r=[distance*math.sin(alpha+gama),distance*math.cos(alpha+gama)] #? à inversé ? comme avant ? 
            r=[distance*math.cos(alpha+gama),distance*math.sin(alpha+gama)] #"normal"
            
            return map.xyToGPS(self.A, r)
            
        elif(i==len(self.listDistance)): # le dernier est sur l'axe B1, B2
            #[x,y]=map.gpsToXY(self.A,self.Bm) 
            #alpha=math.atan2(y,x)
            #[x1,y1]=map.gpsToXY(self.B[0], self.B[1])
            #beta=math.atan2(y1,x1)
            #distanceRoute=math.sqrt(x**2+y**2)
            ##r=[distanceRoute*math.sin(alpha)+r*math.sin(beta),distanceRoute*math.cos(alpha)+r*math.sin(beta)] #avant
            #r=[distanceRoute*math.cos(alpha)+r*math.sin(beta),distanceRoute*math.sin(alpha)+r*math.sin(beta)] #apres
            [xb,yb]=map.gpsToXY(self.porte[0], self.porte[1])
            beta=math.atan2(yb,xb) #azimut B0-B1 angle sur le quel le dernier waypoint se balade
            #r : distance entre Bm et le dernier waypoints dans l'axe de la porte
            x=r*math.cos(beta)
            y=r*math.cos(beta)
            P=map.xyToGPS(self.Bm, [x,y])
            
            return P
            
    def R0ToMap(self,P:list, restreintMap:bool=False):
        [x,y]=gpsToXY(self.zero, P)
        j=int((y-self.largeurRoute)/self.pas)
        
        for k in range(len(self.listDistance)+1):
            if(x>=self.listDistance[k]):
                if(k>0):
                    moyenne=(self.listDistance[k-1]+self.listDistance[k])/2
                    if(x<moyenne):
                        i=k-1
                    else:
                        i=k
                else:
                    i=k
        if(0<=i<len(self.map)):
            if(0<=j<=len(self.map[i])):
                return [i,j]
            else:
                if(not restreintMap):
                    return [i,j]
        else:
            if(not restreintMap):
                return [i,j]
        
    def vent(self, P:list, h:int):
        [i,j]=self.R0ToMap(P, True)
        return self.map[i][j].vent(h)

    def courant(self, P:list, h:int, agran:bool=True):
        [i,j]=self.R0ToMap(P, True)
        return self.map[i][j].courant(h)
    
    def uv(self,P:list, h:int, agran:bool=True):
        [i,j]=self.R0ToMap(P, True)
        return self.map[i][j].uv(h)

        
class Carte(Map): #pour le moment la map est fixe cad la météo est prise à un temps T
    def __init__(self, x:int, y:int, zero:list, pas:float):
        super().__init__(x,y)
        self.quartier=[[[0,0], [x//2, y//2]], [[x//2+1,y//2+1], [x, y]],[[x//2,0], [x, y//2]],[[0,y//2+1], [x//2, y]]]
        self.coef=[]
        self.generate()
        self.zero=zero #la case 0,0 est en zeros[0], zeros[1]
        self.pas=pas #taille d'une case
        
    def generate(self):
        s=[0,0,0,0]
       # plt.subplot(121)
        for i in range(self.x):
            for j in range(self.y):                
                if(iN([i,j], self.quartier[0])):
                    self.map[i,j,0]=10
                    self.map[i,j,1]=40+2*random.random()-1
                    self.map[i,j,2]=37
                    self.map[i,j,3]=2
                    self.map[i,j,4]=110
                    self.map[i,j,5]=4+1*random.random()
                    self.map[i,j,6]=1/(5*60+4*random.random()-2)
                    self.map[i,j,7]=200
                    self.map[i,j,8]=20
                    self.map[i,j,9]=20
                    self.map[i,j,10]=10
                    self.map[i,j,11]=30+1*random.random()
                    s[0]+=1
                 #   plt.plot([i],[j], "or")
                    
                if(iN([i,j], self.quartier[1])):
                    self.map[i,j,0]=20
                    self.map[i,j,1]=5+2*random.random()-1
                    self.map[i,j,2]=37
                    self.map[i,j,3]=2
                    self.map[i,j,4]=110
                    self.map[i,j,5]=4+1*random.random()
                    self.map[i,j,6]=1/(5*60+4*random.random()-2)
                    self.map[i,j,7]=200
                    self.map[i,j,8]=20
                    self.map[i,j,9]=20
                    self.map[i,j,10]=10
                    self.map[i,j,11]=30+1*random.random()
                    s[1]+=1
                #    plt.plot([i],[j], "og")
                    
                if(iN([i,j], self.quartier[2])):
                    self.map[i,j,0]=10
                    self.map[i,j,1]=2+2*random.random()-1
                    self.map[i,j,2]=37
                    self.map[i,j,3]=2
                    self.map[i,j,4]=110
                    self.map[i,j,5]=4+1*random.random()
                    self.map[i,j,6]=1/(5*60+4*random.random()-2)
                    self.map[i,j,7]=200
                    self.map[i,j,8]=20
                    self.map[i,j,9]=20
                    self.map[i,j,10]=10
                    self.map[i,j,11]=30+1*random.random()
                    s[2]+=1
               #     plt.plot([i],[j], "ob")
                    
                if(iN([i,j], self.quartier[3])):
                    self.map[i,j,0]=10
                    self.map[i,j,1]=80+2*random.random()-1
                    self.map[i,j,2]=37
                    self.map[i,j,3]=2
                    self.map[i,j,4]=110
                    self.map[i,j,5]=4+1*random.random()
                    self.map[i,j,6]=1/(5*60+4*random.random()-2)
                    self.map[i,j,7]=200
                    self.map[i,j,8]=20
                    self.map[i,j,9]=20
                    self.map[i,j,10]=10
                    self.map[i,j,11]=30+1*random.random()
                    s[3]+=1
         #           plt.plot([i],[j], "oy")
                    
                self.coef.append([self.map[i,j,k] for k in [0]]) #on ne prend pas les directions 0, 2, 4,5
        
        #print(s)
        #plt.title("r 0, g 1, b 2, y 3")
        #plt.show()
        
    def cluster(self, metric='manhattan')->list:
        #hdb=hdbscan.HDBSCAN(metric=metric).fit(self.coef)
        #A=hdb.labels_
        nb=4
        kmeans = KMeans(n_clusters=nb, random_state=0).fit(self.coef)
        A=kmeans.labels_
        D=[]
        for i in range(nb):#max(A)+2): 
            D.append([])

        i=0
        j=0
        for k in range(len(A)):
            D[A[i]].append([i,j])
            j+=1
            if(j==self.y):
                j=0
                i+=1
        return D
      
    def mapToLatLong(self, i:int, j:int):
        return [4.1,1.1]    
    
    def __generate(self,i,j):
        [lat,lng]=self.mapToLatLong(i,j)
        req=requests.get("https://www.prevision-meteo.ch/services/json/lat=45.32lng=8.54")
        if(req.status_code==200):
            j=req.json()
            #le probleme est la duree dune requete 3s mini soit 6min pour une carte de 10x10 
            #lidee serait de completer la carte au fur et a mesure des requetes
            #de plus pk faire une map complete alors quon ne travail aue sur des perpendiculaires
            #cela a comme but de mieux detecter les profondeurs sinon il faut superposer une carte dinterdiction de zones profondeurs et Aiss
 
    def plot(self, show:bool=True):
        plt.subplot(122)
        D=self.cluster()
        color=["b", "g", "r", "c", "m",  "y", "k"]
        form=[".", "<",">"]
        for i in range(len(D)):
            plt.plot([D[i][j][0] for j in range(len(D[i]))] , [D[i][j][1] for j in range(len(D[i]))], form[i%len(form)]+color[i%len(color)])
        print(len(D))
        print([len(D[i]) for i in range(len(D))])
        if(show):
            plt.show()
        vent=[self.coef[i][0] for i in range(self.x*self.y)]
        
        plt.plot([i for i in range(self.x*self.y)], [self.coef[i][0] for i in range(self.x*self.y)])
        plt.show()
      
    #def profondeur(self, i,j):
    #    return self.map[i,j,0] #profondeur en m >0, si p<0 -> sol 
    #def vent(self, i,j):
    #    return [self.map[i,j,1], self.map[i,j,2]] #vent spd, dir
    #def courant(self, i,j):
    #    return [self.map[i,j,3], self.map[i,j,4]] #courant spd dir
    #def houle(self, i,j):
    #    return [self.map[i,j,5], self.map[i,j,6], self.map[i,j,7]]  #A,f, dir     
    #def air(self, i,j):
    #    return [self.map[i,j,8], self.map[i,j,9]] #T, H
    #def eau(self,i,j):
    #    return [self.map[i,j,10], self.map[i,j,11]] #T, S
    
    def ref0Tomap(self, x,y):
        """x,y coordonnée dans le ref0 rend la case"""
        return [int((x-self.zero[0])//self.pas), int((y-self.zero[1])//self.pas)]

    def mapToref0(self, i,j):
        """i,j case dans la map rend les coordonnées dans ref0"""
        return [self.pas*i+self.zero[0], self.pas*j+self.zero[1]]
        
if __name__ == "__main__":
    A=[[0,0,0,"N"],[0,0,0,"E"]]
    B=[[1,0,0,"N"],[1,0,0,"E"]]
    C=[[1,0,0,"S"],[2,0,0,"W"]]
    Bm=[[0,0,0,"N"],[0,59,59.862,"E"]]
    
    D=[[[1,0,0,"N"],[1,0,0,"E"]],[[1,0,0,"S"],[1,0,0,"E"]]]
    E=[[0,0,0,"N"],[1,0,0,"E"]]
    x=[-43.2964, 43.2964]
    #print(xyToGPS(A,[59.9999*1852,60*1852],False))
    
    F=[[1,0,0,"N"],[0,0,0,"E"]]
    
    
    #carte=Map2(A,F,1852,3*24)
    
    #print(carte.R0ToMap(F, False))
    #print(gpsToXY(A,F, "kns"))
    #[i,j]=carte.R0ToMap(F,False)
    #print("i,j",[i,j],carte.n,carte.m )
    #print("FAvant=", decimauxToSexagesimaux2(carte.MapToR0(i,j)), decimauxToSexagesimaux2(carte.map[i][j].coordonnee), F)
    #carte.agrandissement(C)
    #[i,j]=carte.R0ToMap(F,False)
    #print("i,j",[i,j],carte.n,carte.m )
    #print("FApres=", decimauxToSexagesimaux2(carte.MapToR0(i,j)), decimauxToSexagesimaux2(carte.map[i][j].coordonnee), F)
    #[i,j]=carte.R0ToMap(C,False)
    #print("i,j",[i,j],carte.n,carte.m )
    #print("Bapres=", decimauxToSexagesimaux2(carte.MapToR0(i,j)), decimauxToSexagesimaux2(carte.map[i][j].coordonnee), C)
    #print(decimauxToSexagesimaux2(carte.zero),  decimauxToSexagesimaux2(carte.A))
    #[x0,y0]=gpsToXY(A,D[0])
    #[x1,y1]=gpsToXY(A,D[1])
    #print(x0,y0,"/",x1,y1, "#",(x0+x1)/2,(y0+y1)/2)
    #print(gpsToXY(A,E))
    #print(xyToGPS(A,[(x0+x1)/2,(y0+y1)/2], False))
    #print("distance AB", distanceGPS(A,Bm,1, "km"),"/", distanceGPS(A,Bm,2, "km"),"/",  distanceGPS(A,Bm, 3, "km"))
    
    #t0=time.time()
    # #modifier 
    #print(decimauxToSexagesimaux2(carte.zero), decimauxToSexagesimaux2(carte.A))
    #[i,j]=carte.R0ToMap(A)
    #carte.map[i][j].setData()
    #[i,j]=carte.R0ToMap(B)
    #carte.map[i][j].setData()
    #print("1",carte.R0ToMap(C))
    #print("2",carte.R0ToMap(C))
    #print("new zero",decimauxToSexagesimaux2(carte.zero), "new A",decimauxToSexagesimaux2(carte.A))
    #print(carte.n,carte.m)
    #print(carte.R0ToMap(A), carte.R0ToMap(B), carte.R0ToMap(C, False), carte.R0ToMap(carte.A, False))
    #print(time.time()-t0)
    #print(carte.zero)
    #print(carte.n,carte.m)
    #print(carte.R0ToMap(A))
    #print(carte.R0ToMap(B))
    #print(carte.R0ToMap(C))
    #carte2=Map(A,B,1852,3*24)
    #carte2.agrandissement(C)
