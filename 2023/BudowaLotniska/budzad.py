import numpy as np
import itertools

wolnePasy = {}
pionowe = {}
poziome = {}
jedynki = []
arr = []
maxdl,n,m = 0, 0, 0


def wczytajDaneZPliku():
    global arr, n, m
    output = open('input.txt', 'r')
    n, m = map(int,output.readline().split(" "))
    
    lines = output.readlines()
    output.close()

    arr = np.zeros((n,n))

    for x in range(n):
        for y in range(n):
            if (lines[x][y] == "X"):
                arr[x][y] = 1

def zapiszPas(x, y, poziom = True):
    global wolnePasy, pionowe, poziome, jedynki

    dl = 0
    if poziom:
        dl = y[1] - x[1] + 1
    else:
        dl = y[0] - x[0] + 1
    #print("%s -> %s = %d"%(x, y, dl))
    if dl==1:
        check = np.isin([x,y],jedynki)
        if not (check[0][0] and check[0][1] and check[1][0] and check[1][1]):
            jedynki.append([x,y])
            if dl in wolnePasy:
                wolnePasy[dl] += 1
            else:
                wolnePasy[dl] = 1
    else:
        if poziom:
            if dl in poziome:
                poziome[dl].append([x,y])
            else:
                poziome[dl] = [[x,y]]
        else:
            if dl in pionowe:
                pionowe[dl].append([x,y])
            else:
                pionowe[dl] = [[x,y]]
        if dl in wolnePasy:
            wolnePasy[dl] += 1
        else:
            wolnePasy[dl] = 1

def analizujWejscie():
    jedynki = np.argwhere(arr == 1)
    pop = [-1,-1]
    for j in jedynki:
        if j[0] != pop[0]:
            for i in range(j[0] - pop[0]):
                if pop[0] + i >= 0:
                    if i > 0:
                        zapiszPas([pop[0] + i, 0], [pop[0] + i, n-1])
                    else:
                        if pop[1] < n-1:
                            zapiszPas([pop[0] + i, pop[1]+1], [pop[0] + i, n-1])
            if j[1] > 0:
                zapiszPas([j[0], 0], [j[0], j[1]-1])
        if j[0] == pop[0] and j[1] - pop[1] > 1:
            zapiszPas([pop[0], pop[1]+1], [j[0], j[1]-1])
        pop = j
    if pop[1] < (n-1):
        zapiszPas([pop[0], pop[1]+1], [pop[0], n-1])

    '''odwracam tablicę i szukam pionowych pasów'''
    jedynki = np.argwhere(arr.T == 1)
    pop = [-1,-1]
    for j in jedynki:
        if j[0] != pop[0]:
            for i in range(j[0] - pop[0]):
                if pop[0] + i >= 0:
                    if i > 0:
                        zapiszPas([0,pop[0] + i], [n-1,pop[0] + i], False)
                    else:
                        if pop[1] < n-1:
                            zapiszPas([pop[1]+1, pop[0] + i], [n-1, pop[0] + i], False)
            if j[1] > 0:
                zapiszPas([0, j[0]], [j[1]-1, j[0]], False)
        if j[0] == pop[0] and j[1] - pop[1] > 1:
            zapiszPas([pop[1]+1, pop[0]], [j[1]-1, j[0]], False)
        pop = j
    if pop[1] < (n-1):
        zapiszPas([pop[1]+1, pop[0]], [n-1, pop[0]], False)

def szukajRozwiazania():
    global maxdl
    sortedDict = dict(sorted(wolnePasy.items(), reverse=True))
    for k in sortedDict:
        if m==1:
            '''prosta sprawa - zwracamy najdłuższy pas'''
            maxdl = k
            break
        else:
            if wolnePasy[k] == 2:
                '''mamy dokładnie 2 pasy trzeba sprawdzić czy są równoległe jeśli nie to czy się przecinają'''
                if k not in poziome or k not in pionowe:
                    '''mamy 2 pasy są równoległe'''
                    maxdl = k
                    break
                else:
                    o1 = poziome[k][0]
                    o2 = pionowe[k][0]
                    '''sprawdzenie czy się przecinają'''
                    if not (o2[0][0] <= o1[0][0] and o1[0][0] <= o2[1][0] and o1[0][1] <= o2[0][1] and o2[0][1] <= o1[1][1]):
                        maxdl = k
                        break
                    else:
                        '''jeśli się przecinają to zapisujemy punkt przecięcia jako jedynkę i ocięte przez przecięcie odcinki i szukamy dalej'''
                        '''dopisuję punkt przecięcia'''
                        zapiszPas([o1[0][0], o2[1][1]],[o1[0][0], o2[1][1]], True)
                        '''dopisuję odcinki wyznaczone przez punkt przecięcia'''
                        if o2[1][1] > 0:
                            zapiszPas(o1[0], [o1[0][0], o2[1][1]-1],True)
                        if o2[1][1] < n-1:
                            zapiszPas([o1[0][0], o2[1][1]+1], o1[1],True)
                        if o1[0][0] > 0:
                            zapiszPas(o2[0], [o1[0][0]-1, o2[1][1]], False)
                        if o1[0][0] < n-1:
                            zapiszPas([o1[0][0]+1, o2[1][1]], o2[1], False)
            if wolnePasy[k] > 2:
                '''mamy zawsze co najmniej 2 równoległe o tej samej długości, więc ta długość jest rozwiązaniem'''
                maxdl = k
                break

wczytajDaneZPliku()
analizujWejscie()
szukajRozwiazania()

print(maxdl)
# print(arr)
# print("wolnePasy: %s\npoziome: %s\npionowe: %s\njedynki: %s"%(wolnePasy,poziome,pionowe,jedynki))
