import numpy as np
import itertools

wolnePasy = []
pionowe = {}
poziome = {}
arr = []
maxdl,n,m = 0, 0, 0


def wczytajDaneZPliku():
    global arr, n, m, wolnePasy, poziome
    output = open('input.txt', 'r')
    n, m = map(int,output.readline().split(" "))
    
    lines = output.readlines()
    output.close()
    arr = np.zeros((n,n))
    wolnePasy = np.zeros(n+1,dtype=int)
    pop = 1
    start = [0,0]
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
    
    # print("%s -> %s = %d"%(x, y, dl))
    if dl > 1:
        if poziom:
            if dl in poziome:
                poziome[dl].append((x,y))
            else:
                poziome[dl] = [(x,y)]
        else:
            if dl in pionowe:
                pionowe[dl].append((x,y))
            else:
                pionowe[dl] = [(x,y)]
        wolnePasy[dl] += 1
    
def analizujWejscie():
    global wolnePasy
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
    
    '''wszystkie pola z zerami mogą być pasem o długości 1'''
    wolnePasy[1] = n*n - np.count_nonzero(arr)

def szukajRozwiazania():
    global maxdl
    for k in range(n, 0, -1):
        if m==1 and wolnePasy[k] > 0 or m==2 and wolnePasy[k] > 2:
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
                        '''jeśli się przecinają to dopisujemy składowe odcinków i szukamy dalej'''
                        for i in range(1, o1[1][1] - o1[0][1]):
                            for j in range(i+1, o1[1][1] - o1[0][1] + 1):
                                zapiszPas([o1[0][0], i], [o1[0][0], j], True)
                            zapiszPas(o1[0], [o1[1][0], o1[1][1] - i], True)
                        for i in range(1, o2[1][0] - o2[0][0]):
                            for j in range(i+1, o2[1][0] - o2[0][0] + 1):
                                zapiszPas([i, o2[0][1]], [j, o2[0][1]], False)
                            zapiszPas(o2[0], [o2[1][0] - i, o2[1][1]], False)

wczytajDaneZPliku()
analizujWejscie()
szukajRozwiazania()

print(maxdl)
# print("wolnePasy: %s\npoziome: %s\npionowe: %s"%(wolnePasy,poziome,pionowe))


# print(arr)

# print(np.where(arr == 0))
# print(np.argwhere(arr == 0))
# print(np.argwhere(arr == 0).T)
# it = np.nditer(arr, flags=['multi_index'])
# for x in it:
#     print("%d <%s>" % (x, it.multi_index), end=' ')

