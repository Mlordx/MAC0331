import prim #biblioteca de primitivas geometricas
import point
import math
import sys
####DEFINES#####
N = 100
################



################
pontos = []
pilha = [[int for j in range(N)] for i in range(N) ]

i = 0

hue = []
reflexos = []
ordem = []

for line in sys.stdin:
    hue = line.split()
    bla = point.Point(float(hue[0]),float(hue[1]))
    ordem.append({float(hue[1]),i})
    pontos.append(bla)
    i += 1;


prim.achaReflexos(i,pontos,reflexos)

for bla in reflexos:
    print "[%.1f,%.1f]" % (bla.x,bla.y)

pesos = [[int for b in range(i)] for a in range(i) ]

#comeco triangulando o poligono, deixando apenas as diagonais essenciais
#enquanto usando o algoritmo de triangulacao de monotonos

def angulo(a,b,c):
    A = point.Point(b.x-a.x,b.y-a.y)
    B = point.Point(b.x-c.x,b.y-c.y)
    return math.acos((A.x*B.x + A.y*B.y)/(sqrt(A.x*A.x + A.y*A.y)*sqrt(B.x*B.x+B.y*B.y)))

pilha = []
diagonais = []
verts = sorted(pontos,key=lambda x: x.y, reverse=True)
ordem = sort(key=lambda x:x[0],reverse=True)
"""
pilha.append(verts[0])
pilha.append(verts[1])

for k in range(2,n):
    if(casoA):
        while(t>1 e angulo(verts[i],pilha[t],pilha[t-1]) < pi):
            pilha.pop()
            t -= 1
            diagonais.append({verts[i],pilha[t-1]})
        pilha.append(verts[i])
    if(casoB):
        aux = pilha[t]
        while(t>1):
            diagonais.append({verts[i],pilha[t]})
            pilha.pop()
        pilha.pop()
        pilha.append(aux)
        pilha.append(verts[i])
    if(casoC):
        pilha.pop()
        while(t>2):
            t -= 1
            diagonais.append({verts[i],pilha[t]})
            pilha.pop()


"""

"""
def tipoA(i,j,k):

def mcd(P):
    for x in range(i-1):
        pesos[x][x+1] = -1
        if(diagonal(N,P,x,(x+2)%N)):
            pesos[x][(x+2)%N] = 0
            pilha[x][(x+2)%N].append({x+1,x+1})
            

    for size in range(3,N):
        for ref in reflexos:
            if( ref + size <= N ):
                k = ref + size
                if( diagonal(ref,k) ):
                    if k in reflexos: for j in range(ref+1,k-1): tipoA(i,j,k)
                    else:
                        for ref2 in reflexos:
                            if(ref2 > ref and ref2 < k-1): tipoA(ref,ref2,k)
                            tipoA(ref,k-1,k)


        for ref in reflexos:
            if(size <= ref and ref < n):
                i = ref - size
                if(not(i in reflexos) and diagonal(i,ref)):
                    tipoB(i,i+1,ref)
                    for ref2 in reflexos:
                        if(i+1 < ref2 and ref2 < k):
                            tipoB(i,ref2,ref)
            
        

"""
