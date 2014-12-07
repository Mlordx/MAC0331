#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tree import *
from dcel import *
from tri import *
from geocomp.common.polygon import Polygon
from geocomp.common import prim
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from geocomp.common.point import Point

"""
Implementação do algoritmo de linha de varredura para triangulação de Lee e Preparata(Para depois usar no algoritmo de Hertel e Mehlhorn, mas por enquanto deixo aqui a implementação individual dele)
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BOLD = "\033[1m"
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def pontaParaBaixo(x,pontos):
    if(x[1] == 0): ant = len(pontos)-1
    else: ant = x[1] - 1
    
    if(x[1] == len(pontos)-1): prox = 0
    else: prox = x[1] + 1

    if(pontos[ant][0].y > x[0].y and pontos[prox][0].y > x[0].y): return True
    else: return False

def pontaParaCima(x,pontos):
    if(x[1] == 0): ant = len(pontos)-1
    else: ant = x[1] - 1
    
    if(x[1] == len(pontos)-1): prox = 0
    else: prox = x[1] + 1

    if(pontos[ant][0].y < x[0].y and pontos[prox][0].y < x[0].y): return True
    else: return False

def esquerdaEst(aresta,ponto):
    return left(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def esquerda(aresta,ponto):
    return left_on(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def entre(aresta1,aresta2,ponto):
    if(esquerda(aresta1,aresta2.getAresta().init) ):
        return esquerdaEst(aresta1,ponto) and not esquerdaEst(aresta2,ponto)
    else:
        return not ( esquerda(aresta2,ponto) and not esquerda(aresta1,ponto) )
   

def insereDiagonal(vertice1,vertice2,diagonal,faces):
    e  = vertice2.getAresta().getGemeo() #vertice2 é o final da diagonal a->b
    e2 = vertice1.getAresta().getGemeo()
    aux = aux2 =  None

    faceOriginal = Face(e)
    numArestas = faceOriginal.tamFace()

    while( (e.getProx()).getGemeo() != aux ):
        if(entre(e,(e.getProx()).getGemeo(),diagonal.getAresta().init)):
            bla = e
            bla2 = e.getProx().getGemeo()
            v1 = vertice1.getAresta()

            ########## Procura a aresta e a proxima de v1 na face atual
            while( (e2.getProx()).getGemeo() != aux2 ):
                if(not entre(e2,(e2.getProx()).getGemeo(),diagonal.getAresta().to)):
                    bla3 = e2
                    bla4 = (e2.getProx()).getGemeo()
                e2 = (e2.getProx()).getGemeo()
                if(aux2 is None): aux2 = e2
            ##########

            aux = bla.getGemeo()
            bla = aux

            aux = bla4.getGemeo()
            bla4 = aux


            bla3.setProx(diagonal)
            diagonal.setAnt(bla3)

            diagonal.setProx(bla)
            bla.setAnt(diagonal)

            bla2.setProx(diagonal.getGemeo())
            diagonal.getGemeo().setAnt(bla2)

            diagonal.getGemeo().setProx(bla4)
            bla4.setAnt(diagonal.getGemeo())

            face1 = Face(diagonal)
            face2 = Face(diagonal.getGemeo())

            if((face1.tamFace() + face2.tamFace() - 2) != numArestas): print "OPA! Algo errado nas faces"
            else: print "Tudo certo com as faces criadas!"

            faces.append(face1)
            faces.append(face2)
            break            
        
        e = (e.getProx()).getGemeo()
        if(aux is None): aux = e



def trataCaso1(u,v,w,arvore,pontos,vertices,diagonais,faces):
    if(u.y < w.y): #u <=> w
        aux = w
        w = u 
        u = aux

    aux = (arvore.get(v[0])).trap #aux recebe um trapézio que contem v
    arvore.delete(v[0])
        
    if(v[0].x == aux[0].to.x and v[0].y == aux[0].to.y): 
        arvore.insert((Segment(v[0],w),v,aux[2]))
        print bcolors.OKBLUE,"Inseri um trapézio com vértice de apoio", v," : ",Segment(v[0],w),aux[2],bcolors.ENDC
    else:
        arvore.insert((aux[0],v,Segment(v[0],w)))
        print bcolors.OKBLUE,"Inseri um trapézio com vértice de apoio ",v,": ",aux[0],Segment(v[0],w),bcolors.ENDC

    if(pontaParaBaixo(aux[1],pontos)):
        diagonais.append(Segment(aux[1][0],v[0]))

        aresta = Aresta()
        aresta.setAresta(Segment(aux[1],v))
        aresta2 = Aresta()
        aresta2.setAresta(Segment(v,aux[1]))

        aresta.setGemeo(aresta2)
        aresta2.setGemeo(aresta)

        Segment(aux[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[aux[1][1]-1],vertices[v[1]-1],aresta,faces)
        print "Adicionada diagonal ",Segment(aux[1][0],v[0])

def trataCaso2(u,v,w,arvore,vertices,diagonais,faces):
    if(left(u,v[0],w)): # u<=>w
        aux = w
        w = u
        u = aux

    aux = arvore.get(v[0])
    arvore.delete(v[0])

    if(aux is None):
        print bcolors.OKBLUE,"Inseri um trapézio com vértice de apoio ", v,": ",Segment(v[0],u),Segment(v[0],w),bcolors.ENDC
        arvore.insert( ( Segment(v[0],u),v,Segment(v[0],w) ) )
    else:
        trap = aux.trap
        print bcolors.OKBLUE,"Inseri dois trapézios com vértice de apoio ", v ,": ",trap[0],Segment(v[0],u)," E ",Segment(v[0],w),trap[2],bcolors.ENDC
        arvore.insert( (Segment(v[0],w),v,trap[2]) )  #insiro esse primeiro para respeitar a ordem correta na arvore(dado que eu escolhi comparar por x do vertice de apoio
        arvore.insert( (trap[0],v,Segment(v[0],u)) )

        diagonais.append( Segment(trap[1][0],v[0]) )

        aresta =  Aresta()
        aresta.setAresta(Segment(trap[1],v))
        aresta2 = Aresta()
        aresta2.setAresta(Segment(v,trap[1]))
        
        aresta.setGemeo(aresta2)
        aresta2.setGemeo(aresta)

        Segment(trap[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[trap[1][1]-1],vertices[v[1]-1],aresta,faces)
        print "Adicionada diagonal ", Segment(trap[1][0],v[0])
        
def trataCaso3(v,arvore,pontos,vertices,diagonais,faces):
    aux = (arvore.get(v[0])).trap
    arvore.delete(v[0])

    if(pontaParaBaixo(aux[1],pontos)):#aux[1] = vertice de apoio do trapézio
        diagonais.append(Segment(aux[1][0],v[0]))

        aresta = Aresta()
        aresta.setAresta(Segment(aux[1],v))
        aresta2 = Aresta()
        aresta2.setAresta(Segment(v,aux[1]))

        aresta.setGemeo(aresta2)
        aresta2.setGemeo(aresta)

        Segment(aux[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[aux[1][1]-1],vertices[v[1]-1],aresta,faces)
        print "Adicionada diagonal ",Segment(aux[1][0],v[0])
    
    if((aux[0].to.x != v[0].x and aux[0].to.y != v[0].y) or (aux[2].to.x != v[0].x and aux[2].to.y != v[0].y)):#caso tenham 2 trapézios com v
        aux2 = (arvore.get(v[0])).trap #segundo trapézio que contém v
        arvore.delete(v[0])

        if(pontaParaBaixo(aux2[1],pontos)): #aux2[1] = vertice de apoio do segundo trapézio
            diagonais.append(Segment(aux2[1][0],v[0]))

            aresta = Aresta()
            aresta.setAresta(Segment(aux2[1][0],v[0]))
            aresta2 = Aresta()
            aresta2.setAresta(Segment(v[0],aux2[1][0]))

            aresta.setGemeo(aresta2)
            aresta2.SetGemeo(aresta)

            Segment(aux2[1][0],v[0]).hilight("blue")            
            control.sleep()
            insereDiagonal(vertices[aux2[1][1]-1],vertices[v[1]-1],aresta,faces)
            print "Adicionada diagonal ",Segment(aux2[1][0],v[0])

        if( aux[2].init.x == v[0].x and aux[2].init.y == v[0].y):
            arvore.insert( (aux[0],v,aux2[2]) )
            print bcolors.OKBLUE,"Inserido trapézio com vértice de apoio ",v," : ",aux[0],aux2[2]
        else:
            arvore.insert( (aux2[0],v,aux[2]) )
            print bcolors.OKBLUE,"Inserido trapézio com vértice de apoio ",v,": ",aux2[0],aux[2],bcolors.ENDC

def lp(l):
    #na arvore, cada trapezio é uma tripla (Segmento,(ponto,indice),Segmento), sendo então trapezio[0] o segmento esquerdo, trapezio[2] o direito e trapezio[1] o vértice de apoio

    arvore = Arvore()

    for x in range(len(l)):
        if(x != len(l)-1): l[x].lineto(l[(x+1)],'red')
        else: l[x].lineto(l[0],'red')                                    
    
    N = len(l)
    pontos = [] #lista de pontos, juntamente com seus indices originais
    verts = [] #lista de pontos ordenada
    diagonais = [] #lista das diagonais que particionam o poligono em poligonos menores monótonos

    for i in range(N): pontos.append((l[i],i))
    verts = sorted(pontos,key=lambda x: (x[0].y,-x[0].x), reverse=True)	 

    aux = []
    arestas = []
    arestas2 = []

    for a in range(N):
        if(a != N-1):
            ar = Aresta()
            ar.setAresta(Segment(pontos[a],pontos[a+1]))

            ar2 = Aresta()
            ar2.setAresta(Segment(pontos[a+1],pontos[a]))

            ar.setGemeo(ar2)
            ar2.setGemeo(ar)

            arestas.append(ar)
            arestas2.append(ar2)
            
        else:
            ar = Aresta()
            ar.setAresta(Segment(pontos[a],pontos[0]))

            ar2 = Aresta()
            ar2.setAresta(Segment(pontos[0],pontos[a]))

            ar.setGemeo(ar2)
            ar2.setGemeo(ar)

            arestas.append(ar)
            arestas2.append(ar2)

    for k in range(len(arestas)):
        if(k!= 0 and k!= len(arestas)-1):
            arestas[k].setProx(arestas[k+1])
            arestas[k].setAnt(arestas[k-1])

            arestas2[k].setProx(arestas2[k-1])
            arestas2[k].setAnt(arestas2[k+1])
        elif(k == 0):
            arestas[k].setProx(arestas[k+1])
            arestas[k].setAnt(arestas[len(arestas)-1])

            arestas2[k].setProx(arestas2[len(arestas)-1])
            arestas2[k].setAnt(arestas2[k+1])
        else:
            arestas[k].setProx(arestas[0])
            arestas[k].setAnt(arestas[k-1])

            arestas2[k].setProx(arestas2[k-1])
            arestas2[k].setAnt(arestas2[0])

    for a in range(N):
        bla = Vertice(aresta=arestas2[a])
        aux.append(bla)          
        
    face = Face(arestas2[0])
    faces = []

    faces.append(face)

############## Esse pedaço verifica se o poligono passado já é monotono. Se for ele passa a lista de pontos para o algoritmo de triangulação de monótonos
    monotono = True
    for i in range(1,N-1):
        if(pontaParaBaixo(verts[i],pontos) or pontaParaCima(verts[i],pontos)):
            monotono = False

    if(monotono == True):
        triangulaMonotono(faces[0].listaFace())
        return 0;
################

    for k in range(0,N):
        verts[k][0].hilight("yellow")

        if(verts[k][1] == 0): ant = len(l)-1
        else: ant = verts[k][1]-1

        if(verts[k][1] == len(l)-1): prox = 0
        else: prox = verts[k][1] +1

        pontos[ant][0].hilight("blue")
        pontos[prox][0].hilight("green")
        control.sleep()

        if( (pontos[ant][0].y <= verts[k][0].y and verts[k][0].y < pontos[prox][0].y) or (pontos[prox][0].y <= verts[k][0].y and verts[k][0].y < pontos[ant][0].y) ): #Caso 1: uma aresta acima e outra embaixo
            print "ENTREI NO CASO 1 NO VÉRTICE ", verts[k][0]
            trataCaso1(pontos[ant][0],verts[k],pontos[prox][0],arvore,pontos,aux,diagonais,faces)
        elif(pontos[ant][0].y <= verts[k][0].y): #Caso 2: as duas arestas embaixo
            print "ENTREI NO CASO 2 NO VÉRTICE ",verts[k][0]
            trataCaso2(pontos[ant][0],verts[k],pontos[prox][0],arvore,aux,diagonais,faces)
        else: #Caso 3: as duas arestas em cima
            print "ENTREI NO CASO 3 NO VÉRTICE ", verts[k][0]
            trataCaso3(verts[k],arvore,pontos,aux,diagonais,faces)

        verts[k][0].hilight("red")
        pontos[ant][0].hilight("red")
        pontos[prox][0].hilight("red")


    for bla in faces:
        if( bla != face ):
            triangulaMonotono(bla.listaFace())

    for d in diagonais:
        d.hilight('blue')


        
