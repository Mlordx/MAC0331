import prim #biblioteca de primitivas geometricas
import sys

pontos = [[int for j in range(2)] for i in range(100) ]
i = 0

hue = []
reflexos = []

for line in sys.stdin:
    hue = line.split()
    pontos[i][0] = float(hue[0])
    pontos[i][1] = float(hue[1])
    i += 1;

prim.achaReflexos(i,pontos,reflexos)

for bla in reflexos:
    print "%d: [%.1f,%.1f]" % (bla,pontos[bla][0],pontos[bla][1])



pesos = [[int for b in range(i)] for a in range(i) ]

for x in range(i-1):
    pesos[x][x+1] = -1


