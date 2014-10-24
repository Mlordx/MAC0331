###################################################################################################################################################
def xor(a,b):
    return (a and not b) or (not a and b)

def esquerda(x1,y1,x2,y2,x3,y3):
    if((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1) >= 0 ): return True
    else: return False

def esquerdaEst(x1,y1,x2,y2,x3,y3):
    if((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1) > 0 ): return True
    else: return False

def colinear(x1,y1,x2,y2,x3,y3):
    if((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1) == 0 ): return True
    else: return False

def entre(x1,y1,x2,y2,x3,y3):
    if(not colinear(x1,y1,x2,y2,x3,y3)): return False
    elif(x1 != x2): return ((x1 <= x3) <= x2) or ((x2 <= x3) <= x1)
    else: return ((y1 <= y3) <= y2) or ((y2 <= y3) <= y1)

def intersectaProp(x1,y1,x2,y2,x3,y3,x4,y4):
    if(colinear(x1,y1,x2,y2,x3,y3) or colinear(x1,y1,x2,y2,x4,y4) or colinear(x3,y3,x4,y4,x1,y1) or colinear(x3,y3,x4,y4,x2,y2)): return False
    return xor(esquerdaEst(x1,y1,x2,y2,x3,y3),esquerdaEst(x1,y1,x2,y2,x4,y4)) and xor(esquerdaEst(x3,y3,x4,y4,x1,y1),esquerdaEst(x3,y3,x4,y4,x2,y2))

def intersecta(x1,y1,x2,y2,x3,y3,x4,y4):
    if(intersectaProp(x1,y1,x2,y2,x3,y3,x4,y4)): return True
    return entre(x1,y1,x2,y2,x3,y3) or entre(x1,y1,x2,y2,x4,y4) or entre(x3,y3,x4,y4,x1,y1) or entre(x3,y3,x4,y4,x2,y2)

def noCone(n,P,i,j):#n = numero de vertices, P eh o vetor de pontos, PiPj determina o candidato a diagonal
    u = (i - 1)%n
    w = (i + 1)%n
    if(esquerda(P[u][0],P[u][1],P[i][0],P[i][1],P[w][0],P[w][1])): return esquerdaEst(P[i][0],P[i][1],P[j][0],P[j][1],P[u][0],P[u][1]) and esquerdaEst(P[j][0],P[j][1],P[i][0],P[i][1],P[w][0],P[w][1])
    else: return not(esquerda(P[i][0],P[i][1],P[j][0],P[j][1],P[w][0],P[w][1]) and esquerda(P[j][0],P[j][1],P[i][0],P[i][1],P[u][0],P[u][1]))

def quaseDiagonal(n,P,i,j):
    for k in range(n):
        l = (k+1)%n
        if(k!=i and k!= j and l != i and l != j): 
            if(intersecta(P[i][0],P[i][1],P[j][0],P[j][1],P[k][0],P[k][1],P[l][0],P[l][1])): return False
    return True

def diagonal(n,P,i,j):
    return noCone(n,P,i,j) and quaseDiagonal(n,P,i,j)

##################################################################################################################################################

def achaReflexos(n,P,R):
    compara = esquerda(P[n-1][0].x,P[n-1][0].y,P[1][0].x,P[1][0].y,P[0][0].x,P[0][0].y)
    i = 1
    while i < n:
        j = (i-1)%n
        k = (i+1)%n
        aux = esquerda(P[j][0].x,P[j][0].y,P[k][0].x,P[k][0].y,P[i][0].x,P[i][0].y)
        if(aux != compara):
            #print "O ponto %d eh reflexo" % i
            #compara = aux
            R.append(P[i])
        i += 1
