#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.prim import *

"""
Implementação de árvore de busca binária para uso no algoritmo de linha de varredura de Lee e Preparata.
"""

class Folha:#uso folha no sentido de elemento da árvore, e não necessariamente um nó sem vizinhos.
    def __init__(self,trap,left=None,right=None,parent=None): 
        self.trap = trap #trapezio contido naquela folha
        self.l = left #nó esquerdo
        self.r = right #nó direito
        self.parent = parent #nó pai
    
    def replace(self,key,lc,rc): #substitui folha
        self.trap = key
        self.l = lc
        self.r = rc
        if(self.l is not None): 
            self.l.parent = self
        if(self.r is not None):
            self.r.parent = self
    
class Arvore:
    def __init__(self):
        self.size = 0
        self.raiz = Folha(None)

    def length(self): #função que devolve o tamanho
        return self.size

    def __len__(self): #overload no operador de tamanho
        return self.size
    
    def insert(self,x): #caso já haja raiz insere na árvore por recursão, senão apenas coloca o trapézio novo como raiz
        if(self.size > 0):
            self._insert(x,self.raiz)  
        else:
            self.raiz = Folha(x)
        self.size += 1

    def _insert(self,x,v):
        if(x[1][0].x <= v.trap[1][0].x):
            if(v.l is None):
                v.l = Folha(x,parent=v)
            else:
                self._insert(x,v.l)
        else:
            if(v.r is None):
                v.r = Folha(x,parent=v)
            else:
                self._insert(x,v.r)

    def contains(self,x,trap): #Checa se o trapézio do nó atual da árvore contém o ponto x
        if(trap[0].init.x == x.x and trap[0].init.y == x.y) or (trap[0].to.x == x.x and trap[0].to.y == x.y) or (trap[2].init.x == x.x and trap[2].init.y == x.y) or (trap[2].to.x == x.x and trap[2].to.y == x.y): return True  #caso ele esteja nas pontas de uma das arestas do trapézio
        elif(x.x == trap[1][0].x and x.y == trap[1][0].y): return True #caso ele seja o vértice de apoio
        elif( ((x.x >= trap[0].to.x) and x.x <= trap[2].to.x) and ((x.y <= trap[0].init.y and x.y >= trap[0].to.y) or (x.y <= trap[2].init.y or x.y >= trap[2].to.y) ) ): return True #caso ele esteja na área contida entre as arestas + vértice de apoio
        return False #caso não esteja no trapézio

    def get(self,x):#acha primeiro trapezio na árvore que contém o vértice x
        if(self.size == 0): return None
        else:
            res = self._get(x,self.raiz)
            return res
        
    def _get(self,x,v):
        if(v is None): 
            return v
        if(self.contains(x,v.trap)): 
            return v
        if(x.x <= v.trap[1][0].x):
            return self._get(x,v.l)
        else:
            return self._get(x,v.r)

    def delete(self,x): #remove o primeiro trapézio encontrado com o Ponto x contido nele
        if(self.size > 1):
            r = self._get(x,self.raiz)
            if(r is not None):
                self.remove(r)
                self.size -= 1
        elif(self.size == 1 and self.contains(x,self.raiz.trap)): #caso o trapézio a ser removido fosse o único na árvore
            #print "removi o trapezio : ",self.raiz.trap[0],self.raiz.trap[1],self.raiz.trap[2]
            self.raiz = None
            self.size -= 1

    def __delitem__(self,x):
        self.delete(x)
        
    def getMin(self): #acha o menor elemento da árvore
        x = self.raiz
        while(x.l):
            x = x.l
        return x

    def findSuccessor(self,hue): #acha o elemento que melhor substituiria o elemento retirado na arvore 
        s = None
        if(hue.r):
            s = self.getMin()
        else:
            hue.parent.r = None
            s = hue.parent.findSuccessor()
            hue.parent.r = hue
        return s

    def spliceOut(self,x): #retira diretamente sem precisar de recursão
        if(not(x.l or x.r)):
            if(x.parent.l == x):
                x.parent.l = None
            else:
                x.parent.r = None
        elif(x.l or x.r):
            if(x.parent and x.parent.l == x):
                x.parent.l = x.l
            else:
                x.parent.r = x.l
                x.l.parent = x.parent
        else:
            if(x.parent and x.parent.l == x):
                x.parent.l = x.r
            else:
                x.parent.r = x.r
                x.r.parent = x.parent
            
    def remove(self,x):
        #print "removi o trapezio : ",x.trap[0],x.trap[1],x.trap[2]
        if(not(x.l or x.r)): #x é folha
            if(x == x.parent.l):
                x.parent.l = None
            else:
                x.parent.r = None
        elif(x.l and x.r): #x tem os dois filhos
            s = self.findSuccessor(x)
            self.spliceOut(s)
            x = s
        else:
            if(x.l is not None):
                if(x.parent and x == x.parent.l): #é filho esquerdo
                    x.l.parent = x.parent
                    x.parent.l = x.l
                elif(x.parent and x == x.parent.r): #é filho direito
                    x.r.parent = x.parent
                    x.parent.r = x.r
                else:   #x era a raiz
                    x.replace(x.l.trap,x.l.l,x.l.r)
            else:
                if(x.parent and x == x.parent.l): #é filho esquerdo
                    x.r.parent = x.parent
                    x.parent.l = x.r
                elif(x.parent and x == x.parent.r): #é filho direito
                    x.r.parent = x.parent
                    x.parent.r = x.r
                else: 
                    x.replace(x.r.trap,x.r.l,x.r.r)
