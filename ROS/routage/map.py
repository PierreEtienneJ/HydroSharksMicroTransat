import numpy as np
import random

import matplotlib.pyplot as plt
import math

import statistics
import time
import sys 
import json
import requests 


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



class Map: ###comme Map mais avec un verrou d'écriture sur l'agrandissement, faut-il le mettre sur la lecture ? 
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
                
                
                if(sexagesimauxToDecimaux2(self.coordonnee)[0]<0): #hémisfère sud 
                    self.content[2,h]=180       #vent sud
                    self.content[1,h]=60     #vent spd
                    self.content[12,h]=2 #uv
                    #sys.stdout.write("vent est \n")
                    #sys.stdout.flush()
                else:
                    self.content[2,h]=180      #vent Sud
                    self.content[1,h]=30     #vent spd
                    self.content[12,h]=7
                
                self.content[3,h]=random.random()*2-1+3     #courant spd
                self.content[4,h]=random.random()*4-2+90     #courant dir
                self.content[5,h]=random.random()*2-1+2     #houle A
                self.content[6,h]=random.random()*2+1     #houle freq
                self.content[7,h]=random.random()*5+90     #houle dir
                self.content[8,h]=20     #T air
                self.content[9,h]=50     #H air
                self.content[10,h]=12    #T eau
                self.content[11,h]=34    #S eau
                #self.content[12,h]=random.randint(6,12) #uv
        self.gen=True
        