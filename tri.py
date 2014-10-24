import math
import point

pilha = []
diagonais = []

epsilon = 0.0000001


def tam(a):
    return (a.x**2 + a.y**2 )**0.5

def angulo(a,b):
    return math.acos((a.x*b.x + a.y*b.y)/(tam(a)*tam(b)))

def vetor(a,b):
    return point.Point(a.x-b.x,a.y-b.y)



def triangulaMonotono(verts,N):
    pilha.append(verts[1])
    pilha.append(verts[0])

    for i in range(2,N):
        t = len(pilha)
   #A ########################
        if(((i-1) == pilha[t-1][1] and (i+1) != pilha[0][1]) or ((i-1) != pilha[0][1] and (i+1) == pilha[t-1][1])): #adjacente a St mas nao a S1
#            print "Entrei no caso A"
            while(t>1 and  angulo(vetor(pilha[t-1][0],verts[i][0]),vetor(pilha[t-1][0],pilha[t-2][0])) <= (math.pi-epsilon)):
                pilha.pop()
                t -= 1
                diagonais.append((verts[i][0],pilha[t-2][0]))
            pilha.append(verts[i])
   #B ########################
        if(((i-1) != pilha[t-1][1] and (i+1) == pilha[0][1]) or ((i-1) == pilha[0][1] and (i+1) != pilha[t-1][1])): #adjacente a S1 mas nao a St
 #           print "Entrei no caso B"
            aux = pilha[t-1]
            while(t>1):
                diagonais.append((verts[i][0],pilha[t-1][0]))
                pilha.pop()
                t -= 1
            pilha.pop()
            pilha.append(aux)
            pilha.append(verts[i])
   #C ########################
        if(((i-1) == pilha[t-1][1] and (i+1) == pilha[0][1]) or ((i-1) == pilha[0][1] and (i+1) == pilha[t-1][1])): #adjacente a St e S1
  #          print "Entrei no caso C"
            pilha.pop()
            while(t>2):
                t -= 1
                diagonais.append((verts[i][0],pilha[t-1][0]))
                pilha.pop()

    for bla in diagonais: print bla
