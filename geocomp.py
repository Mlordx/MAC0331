import prim #biblioteca de primitivas geometricas
import point
import tri
import sys
####DEFINES#####
N = 100
################



################
pontos = [  ]

i = 0

hue = []
reflexos = []

for line in sys.stdin:
    hue = line.split()
    bla = point.Point(float(hue[0]),float(hue[1]))
    pontos.append((bla,i+1))
    i += 1;


#prim.achaReflexos(i,pontos,reflexos)
"""
for bla in reflexos:
    print "[%.1f,%.1f]" % (bla[0].x,bla[0].y)
"""

pesos = [[int for b in range(i)] for a in range(i) ]

#comeco triangulando o poligono, deixando apenas as diagonais essenciais
#enquanto usando o algoritmo de triangulacao de monotonos



verts = sorted(pontos,key=lambda x: x[0].y, reverse=True)


tri.triangulaMonotono(verts,i)

#tri.triangulaMonotono2(verts,i)
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
