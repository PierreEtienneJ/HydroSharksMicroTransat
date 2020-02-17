import numpy as np 
import random
import matplotlib.pyplot as plt
from enum import Enum
#class Error(Enum,Exception):
#    e_Null=0 #Pas d'erreur
#    e_Lenght=1 #Erreur de taille de graph
#    e_Point=2 #point inconnu
#    e_Gen=3 #Erreur génération
#    e_Voisin=4 #voisin inconnu
    
class Graf:
    def __init__(self, height :int, widht:int, zero:float=0):
        self.size=[height, widht]
        self.graf=np.zeros((height, widht,9,2)) #x,y,cout pour x+i,y+j (i,j)€{-1,0,1}, phéromone ou autre
                                                #voisin : (i,j+1),(i-1,j+1),(i-1,j), (i-1,j-1), (i,j-1),(i+1,j-1), (i+1,j),(i+1,j+1)
        self.voisin=[[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
        self.zero=zero
        self.generate()
        #self.error=Error.e_Null
        
    def generate(self, fct=None):
        if(fct==None):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for k in range(8):
                        self.graf[i,j,k,0]=random.random()
                        self.graf[i,j,k,1]=self.zero
        
    def CoutVoisin(self,A:list, B:list)->float: #B voisin de A
        C=[A[0]-B[0],A[1]-B[1]]
        try:
            return self.graf[A[0],A[1],self.voisin.index(C),0]
            pass
        except :
            return None
            pass
        

    def CoutTot(self,A:list)->float: 
        """A liste des sommets pas lesquel on passe""" 
        s=0
        for i in range(len(A)-1):
            s+=self.CoutVoisin(A[i],A[i+1])
        return s
    
    def addCoefVoisin(self,A:list,B:list,coef:float):
        C=[A[0]-B[0],A[1]-B[1]]
        try:
            self.graf[A[0],A[1],self.voisin.index(C),1]+=coef
            pass
        except:
            pass
        
    def getVoisins(self, A:list)->list:
        V=[[A[0]+self.voisin[i][0],A[1]+self.voisin[i][1]] for i in range(len(self.voisin))]
        for e in V:
            if(e[0]<0 or e[0]>=self.size[0] or e[1]<0 or e[1]>=self.size[1]):
                V.pop(e)
        return V
        
    def setCoefSommet(self,P:list, coef:float):
        self.graf[P[0], P[1], 8,0]=coef
    
    def getCoefSommet(self,P:list):
        return self.graf[P[O], P[1], 8,0]
    
    def removeCoefVoisin(self,A:list,B:list, coef:float, restePositif:bool):
        C=[A[0]-B[0],A[1]-B[1]]
        try:
            self.graf[A[0],A[1],self.voisin.index(C),1]-=coef
            pass
        except:
            pass
        
        if(restePositif and self.graf[A[0],A[1],self.voisin.index(C),1]<self.zero):
            self.graf[A[0],A[1],self.voisin.index(C),1]=self.zero