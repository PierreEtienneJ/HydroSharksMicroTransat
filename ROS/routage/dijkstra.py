import graf

class Dijkstra:
    def __init__(self, graf:Graf, A:list, B:list):
        self.graf=graf
        self.A=A
        self.B=B
        self.X=[[i,j] for i in range(self.graf.size[0]) for j in range(self.graf.size[1])] #liste des sommets
        self.E=[]   #liste des sommets déja traité
        
        #on met les coefs des sommets du graf à 1e+100
        #sauf le point A
        for e in self.X:
            self.graf.setCoefSommet(e, 1.0e+100)
        self.graf.setCoefSommet(A,0)
        
    def generate(self):
        while X!=[]:
            a=self.minIn(self.X)[0] #a la première boucle a=A
            self.X.pop(a)
            self.E.append(a)
            if(a==self.B):
                break
            for V in self.graf.getVoisins(a):
                if(V not in E):
                    if(self.graf.getCoefSommet(V)>self.graf.getCoefSommet(a)+self.graf.CoutVoisin(a,V)):
                        self.graf.setCoefSommet(V,self.graf.getCoefSommet(a)+self.graf.CoutVoisin(a,V))
                        ###je sais pas quoi mettre
    
    def solution(self)->list:
        chemin=[A]
        while chemin[-1]!=self.B:
            V=self.minIn(self.graf.getVoisins(A))[1]
            if(V in chemin):
                voisins=self.graf.getVoisins(A)
                voisins.pop(V)
                V=self.minIn(voisins)[1]
            chemin.append(V)
        return chemin
    
    def minIn(self, T, reves=False:bool)->list: #rend l'indice minimum 
        T=[[self.graf.getCoefSommet(T[i]),T[i]] for i in range(len(T))] #liste des couts avec indice
        element = lambda T: T[0]
        T=sorted(T,key=element,reverse=reves) #on fait le trie sur la 1er colone de la matrice
        return T[0]
    