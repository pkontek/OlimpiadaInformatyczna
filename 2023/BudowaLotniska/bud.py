import sys
import numpy as np

wolnePasy = []
pionowe = {}
poziome = {}
arr = []
maxdl,n,m = 0, 0, 0

def wczytajTablice(lines):
    global arr, wolnePasy
    arr = np.zeros((n,n))
    wolnePasy = np.zeros(n+1,dtype=int)
    pop = 1
    start = [0,0]
    for x in range(n):
        for y in range(n):
            if (lines[x][y] == "X"):
                arr[x][y] = 1

def wczytajDaneZPliku():
    global n, m
    input = open('input.txt', 'r')
    n, m = map(int,input.readline().split(" "))
    
    lines = input.readlines()
    input.close()
    
    wczytajTablice(lines)
    
def wczytajDaneZStdin():
    global n, m
    input = sys.stdin
    n, m = map(int,input.readline().split(" "))
    lines = input.readlines()
    
    wczytajTablice(lines)

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
    if pop[0] < (n-1):
        zapiszPas([n-1, 0], [n-1, n-1])

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
    if pop[0] < (n-1):
        zapiszPas([0, n-1], [n-1, n-1], False)
    '''wszystkie pola z zerami mogą być pasem o długości 1'''
    wolnePasy[1] = n*n - np.count_nonzero(arr)

def szukajRozwiazania():
    global maxdl
    for k in range(n, 0, -1):
        if wolnePasy[k] > 0:
            if m==1 or m==2 and wolnePasy[k] > 2:
                '''prosta sprawa - zwracamy najdłuższy pas'''
                maxdl = k
                break
            else:
                if wolnePasy[k] == 2:
                    '''mamy dokładnie 2 pasy trzeba sprawdzić czy są równoległe jeśli nie to czy się przecinają'''
                    if k not in poziome or k not in pionowe:
                        '''mamy 2 pasy które są równoległe'''
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
                            for i in range(1, o1[1][1] - o1[0][1]): #poziome
                                for j in range(i+1, o1[1][1] - o1[0][1] + 1):
                                    zapiszPas([o1[0][0], i], [o1[0][0], j], True)
                                zapiszPas(o1[0], [o1[1][0], o1[1][1] - i], True)

                            for i in range(1, o2[1][0] - o2[0][0]): #pionowe
                                for j in range(i+1, o2[1][0] - o2[0][0] + 1):
                                    zapiszPas([i, o2[0][1]], [j, o2[0][1]], False)
                                zapiszPas(o2[0], [o2[1][0] - i, o2[1][1]], False)
                else:
                    '''wolnePasy[k] == 1'''
                    '''trzeba sprawdzić czy z jakimś mniwszym nie tworzy rozwiązania'''
                    if k > 2 and k in poziome:
                        o1 = poziome[k][0]
                        podzial = int(k/2)
                        korekta = 0
                        '''sprawdzam następne najdłuższe'''
                        for r in range(k-1, podzial, -1):
                            if wolnePasy[r] > 0:
                                if r in poziome: 
                                    '''na pewno się nie przetną'''
                                    podzial = r
                                    break
                                else:
                                    o2 = pionowe[r][0]
                                    if wolnePasy[r] > 1 or not (o2[0][0] <= o1[0][0] and o1[0][0] <= o2[1][0] and o1[0][1] <= o2[0][1] and o2[0][1] <= o1[1][1]):
                                        '''są dwa w pionie lub nie przecinają się'''
                                        podzial = r - 1
                                        break
                                    else:
                                        '''przecinają się, sprawdzam czy po przecięciu zostanie nam wystarczająco długi odcinek'''
                                        p = o2[0][1] - o1[0][1]
                                        if p >= r or (k - p - 1) >= r:
                                            podzial = p 
                                            korekta = 1
                                            break
                        zapiszPas(o1[0], [o1[0][0], o1[0][1] + podzial-1], True)
                        zapiszPas([o1[0][0], o1[0][1] + podzial + korekta], o1[1], True)
                    if k > 2 and k in pionowe:
                        o2 = pionowe[k][0]
                        podzial = int(k/2)
                        korekta = 0
                        '''sprawdzam następne najdłuższe'''
                        for r in range(k-1, podzial, -1):
                            if wolnePasy[r] > 0:
                                if r in pionowe: 
                                    '''na pewno się nie przetną'''
                                    podzial = r 
                                    break
                                else:
                                    o1 = poziome[r][0]
                                    if wolnePasy[r] > 1 or not (o2[0][0] <= o1[0][0] and o1[0][0] <= o2[1][0] and o1[0][1] <= o2[0][1] and o2[0][1] <= o1[1][1]):
                                        '''są dwa w pionie lub nie przecinają się'''
                                        podzial = r - 1
                                        break
                                    else:
                                        '''przecinają się, sprawdzam czy po przecięciu zostanie nam wystarczająco długi odcinek'''
                                        p = o1[0][0] - o2[0][0] 
                                        if p >= r or (k - p - 1) >= r:
                                            podzial = p 
                                            korekta = 1
                                            break
                        # print("k: %s, r: %s, podzial: %s, korekta: %s"%(k,r,podzial,korekta))
                        # print([o2[0], [o2[0][0] + podzial - 1, o2[0][1]]])
                        # print([[o2[0][0] + podzial + korekta, o2[0][1]], o2[1]])
                        zapiszPas(o2[0], [o2[0][0] + podzial - 1, o2[0][1]], False)
                        zapiszPas([o2[0][0] + podzial + korekta, o2[0][1]], o2[1], False)
                                


wczytajDaneZStdin()
# wczytajDaneZPliku()
analizujWejscie()
# print("wolnePasy: %s\npoziome: %s\npionowe: %s"%(wolnePasy,poziome,pionowe))

szukajRozwiazania()

# print(arr)
# print("wolnePasy: %s\npoziome: %s\npionowe: %s"%(wolnePasy,poziome,pionowe))

print(maxdl)


# print(arr)

# print(np.where(arr == 0))
# print(np.argwhere(arr == 0))
# print(np.argwhere(arr == 0).T)
# it = np.nditer(arr, flags=['multi_index'])
# for x in it:
#     print("%d <%s>" % (x, it.multi_index), end=' ')

