import sys
import numpy as np
import pathlib

wolnePasy = []
odcinki = {}
arr = []
maxdl,n,m = 0, 0, 0

def odcinkiRownolegle(odc1, odc2):
    if (odc1[0][0] == odc1[1][0] and odc2[0][0] == odc2[1][0]) or (odc1[0][1] == odc1[1][1] and odc2[0][1] == odc2[1][1]):
        return True
    else:
        return False

def odcPoziomy(odc):
    return odc[0][0] == odc[1][0]

def odcinkiPrzecinajaSie(odc1, odc2):
    if not odcinkiRownolegle(odc1, odc2):
        if odcPoziomy(odc1):
            poziomy = odc1 
            pionowy = odc2
        else:
            poziomy = odc2
            pionowy = odc1
        if poziomy[0][0] >= pionowy[0][0] and poziomy[0][0] <= pionowy[1][0] and poziomy[0][1]<= pionowy[0][1] and poziomy[1][1] >= pionowy[0][1]:
            return True, (poziomy[0][0], pionowy[0][1])
    return False, ()

def dlugoscOdc(odc):
    dl = 0
    if odcPoziomy(odc):
        dl = odc[1][1] - odc[0][1] + 1
    else:
        dl = odc[1][0] - odc[0][0] + 1
    return dl

def maxDlPasa(odc1, odc2):
    maxdl = 0
    '''o1 nie krótszy niż o2'''
    if odcinkiRownolegle(odc1, odc2):
        '''wygrywa krótszy odcinek'''
        maxdl = min(dlugoscOdc(odc1), dlugoscOdc(odc2))
    else:
        przecinka, pp = odcinkiPrzecinajaSie(odc1, odc2)
        if not przecinka:
            maxdl = min(dlugoscOdc(odc1), dlugoscOdc(odc2))
        else:
            if odcPoziomy(odc1):
                poziomy = odc1
                pionowy = odc2
            else:
                poziomy = odc2
                pionowy = odc1
            if pp[0] > pionowy[0][0]:
                maxdl = max(maxdl, maxDlPasa(poziomy, (pionowy[0], (pp[0] - 1, pp[1]))))
            if pp[0] < pionowy[1][0]:
                maxdl = max(maxdl, maxDlPasa(poziomy, ((pp[0] + 1, pp[1]), pionowy[1])))
            if pp[1] > poziomy[0][1]:
                maxdl = max(maxdl, maxDlPasa((poziomy[0], (pp[0], pp[1] - 1)), pionowy))
            if pp[1] < poziomy[1][1]:
                maxdl = max(maxdl, maxDlPasa(((pp[0], pp[1] + 1), poziomy[1]), pionowy))
    '''chyba że dłuższy jest ponad dwa razy dłuższy od tego co nam wyszło'''
    return max(int(dlugoscOdc(odc1) / 2), int(dlugoscOdc(odc2) / 2), maxdl)

def wczytajTablice(lines):
    global arr
    arr = np.zeros((n,n))
    pop = 1
    start = [0,0]
    for x in range(n):
        for y in range(n):
            if (lines[x][y] == "X"):
                arr[x][y] = 1

def wczytajDaneZPliku(path):
    global n, m
    input = open(path, 'r')
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

def odcMa0ZaSasiada(odc):
    global arr
    if dlugoscOdc(odc) == 1:
        x = odc[0][0]
        y = odc[0][1]
        if x > 0 and arr[x-1][y] == 0:
            return True
        if y > 0 and arr[x][y-1] == 0:
            return True
        if x < n - 1 and arr[x+1][y] == 0:
            return True
        if y < n - 1 and arr[x][y+1] == 0:
            return True
    return False

def zapiszOdcinek(odc, poziom = True):
    global wolnePasy, odcinki

    dl = dlugoscOdc(odc)
    # print("%s = %d"%(odc, dl))
    if dl > 1:
        '''ponieważ osobno skanujemy pion i poziom, dla punktów (dl==1) trzeba sprawdzić czy sąsiaduje z innym zerem jeśli tak to nie dopisujemy'''
        if dl in odcinki:
            odcinki[dl].append(odc)
        else:
            odcinki[dl] = [odc]
        wolnePasy[dl] += 1
    else:
        if poziom and not odcMa0ZaSasiada(odc):
            if dl not in odcinki:
                odcinki[dl] = [odc]
                wolnePasy[dl] += 1
            else:
                odcinki[dl].append(odc)
                wolnePasy[dl] += 1
   
def analizujWejscie():
    global wolnePasy
    
    wolnePasy = np.zeros(n+1,dtype=int)

    jedynki = np.argwhere(arr == 1)
    pop = [-1,-1]
    for j in jedynki:
        if j[0] != pop[0]:
            for i in range(j[0] - pop[0]):
                if pop[0] + i >= 0:
                    if i > 0:
                        zapiszOdcinek([[pop[0] + i, 0], [pop[0] + i, n - 1]])
                    else:
                        if pop[1] < n-1:
                            zapiszOdcinek([[pop[0] + i, pop[1] + 1], [pop[0] + i, n - 1]])
            if j[1] > 0:
                zapiszOdcinek([[j[0], 0], [j[0], j[1] - 1]])
        if j[0] == pop[0] and j[1] - pop[1] > 1:
            zapiszOdcinek([[pop[0], pop[1] + 1], [j[0], j[1] - 1]])
        pop = j
    if pop[1] < (n-1):
        zapiszOdcinek([[pop[0], pop[1]+1], [pop[0], n-1]])
    if pop[0] < (n-1):
        for i in range(pop[0] + 1, n):
            zapiszOdcinek([[i, 0], [i, n-1]])
    
    '''odwracam tablicę i szukam pionowych pasów'''
    jedynki = np.argwhere(arr.T == 1)
    pop = [-1,-1]
    for j in jedynki:
        if j[0] != pop[0]:
            for i in range(j[0] - pop[0]):
                if pop[0] + i >= 0:
                    if i > 0:
                        zapiszOdcinek([[0,pop[0] + i], [n-1,pop[0] + i]], False)
                    else:
                        if pop[1] < n-1:
                            zapiszOdcinek([[pop[1]+1, pop[0] + i], [n-1, pop[0] + i]], False)
            if j[1] > 0:
                zapiszOdcinek([[0, j[0]], [j[1]-1, j[0]]], False)
        if j[0] == pop[0] and j[1] - pop[1] > 1:
            zapiszOdcinek([[pop[1]+1, pop[0]], [j[1]-1, j[0]]], False)
        pop = j
    if pop[1] < (n-1):
        zapiszOdcinek([[pop[1]+1, pop[0]], [n-1, pop[0]]], False)
    if pop[0] < (n-1):
        for i in range(pop[0] + 1, n):
            zapiszOdcinek([[0, i], [n-1, i]], False)

def szukajRozwiazania():
    global maxdl, stos
    maxdl = 0
    ind = np.where(wolnePasy > 0)[0][::-1]
    if len(ind) > 0:
        if m == 1:
            maxdl = ind[0]
        if m==2:
            maxPas = ind[0]
            if wolnePasy[maxPas] >2:
                '''więcej niż 2 pasy w najdłuższej długości - nie trzeba szukać dalej'''
                maxdl = maxPas
            if wolnePasy[maxPas] == 2 and (maxPas ==1 or odcinkiRownolegle(odcinki[maxPas][0], odcinki[maxPas][1])):
                '''dwa tej samej długości i równoległe'''
                maxdl = maxPas
            else:
                '''aby znaleźć rozwiązanie wystarczy przeanalizować 3 najdłuższe odcinki, bo wśród 3 odcinków zawsze przynajmniej 2 są równoległe'''
                '''musimy rozważać po kolei od najdłuższego'''
                '''jeśli się przecinają to sprawdzać długości po przecięciu'''
                '''należy sprawdzić też czy długośc kolejnego odcinka nie jest mniejsza od połowy bieżącego'''
                o = []
                cnt = 0
                for i in ind:
                    for odc in odcinki[i]:
                        o.append(odc)
                        cnt += 1
                        if cnt >=3:
                            break
                    if cnt >=3:
                        break
                if len(o) == 1:
                    maxdl = int(dlugoscOdc(o[0])/2)
                else:
                    maxdl = maxDlPasa(o[0],o[1])
                    if len(o) > 2 and dlugoscOdc(o[2]) > maxdl:
                        maxdl = max(maxdl, maxDlPasa(o[0],o[2]),maxDlPasa(o[1],o[2]))
                
wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('%s/testy/in/test44.in'%pathlib.Path(__file__).parent.resolve())

analizujWejscie()

# print(arr)
# print("wolnePasy: %s\nodcinki: %s"%(wolnePasy, odcinki))

szukajRozwiazania()

print(maxdl)
