import sys
import numpy as np
import pathlib
import itertools

n,m = 0,0
przyciski = []
wierszeZDwomaPrzyciskami = []
ilePrzyciskowWWierszu = []
ilePrzyciskowWKolumnie = []
przyciskiWWierszu = []
przyciskiWKolumnie = []
V = 0

def wczytajDaneZPliku(path):
    global n, m
    input = open(path, 'r')
    n, m = map(int,input.readline().split(" "))
    lines = input.readlines()
    input.close()
    
    zaladujTablice(lines)
   
def wczytajDaneZStdin():
    global n, m
    input = sys.stdin
    n, m = map(int,input.readline().split(" "))
    lines = input.readlines()

    zaladujTablice(lines)

def daSieAktywowacParzyste():
    '''
    
    AKTYWNE PARZYSTE 
    a. aktywowanie parzystych przycisków będzie możliwe jeśli istnieją przyciski co najmniej 2 przyciski w jednym rzędzie mające swój odpowiednik w drugim rzędzie. Np.:
    o o -    o - - o    - - - -  
    - - -    - - - -    - o o -
    o o -    o - - o    - o o -
             - - - -    - - - -
    
    b. jest jeszcze taki przypadek:
    - - o o    - - o o
    - - - -    - - - - 
    o - o -    o - - o 
    o - - o    o - o -

    zauważmy, że da się aktywować parzyste jeśli graf zbudowany poprzez połączenie przycisków leżących w jednym wierszu i leżących w jednej kolumnie będzie cykliczny.

    '''
    graf = dict()
    
    for w in przyciskiWWierszu:
        if not w is None and len(w) > 1:
            poprz = w[0]
            for nast in w[1:]:
                dodajDoGrafu(graf, poprz, nast)
                poprz = nast
    for k in przyciskiWKolumnie:
        if not k is None and len(k) > 1:
            poprz = k[0]
            for nast in k[1:]:
                dodajDoGrafu(graf, poprz, nast)
                poprz = nast

    return grafMaCykl(graf)

def dodajDoGrafu(graf, prz1, prz2):
    if prz1 not in graf:
        graf.update({prz1 : [prz2]})
    else:
        graf[prz1].append(prz2)
    if prz2 not in graf:
        graf.update({prz2 : [prz1]})
    else:
        graf[prz2].append(prz1)

def grafMaCykl(graf):
    visited = [False]*(V)

    for i in range(V):
        # Don't recur for u if it
        # is already visited
        if visited[i] == False:
            if(isCyclicUtil(graf, i, visited, -1)) == True:
                return True

    return False

def isCyclicUtil(graf, v, visited, parent):
 
    visited[v] = True
    
    #jeśli węzła nie ma w grafie - to znaczy że nie ma powiązań z innymi
    if v in graf.keys():

        # Recur for all the vertices
        # adjacent to this vertex
        for i in graf[v]:

            # print("i:%s , v: %s"%(i,v))

            # If the node is not
            # visited then recurse on it
            if visited[i] == False:
                if(isCyclicUtil(graf, i, visited, v)):
                    return True
            # If an adjacent vertex is
            # visited and not parent
            # of current vertex,
            # then there is a cycle
            elif parent != i:
                return True

    return False

    
    
def daSieAktywowacNieparzyste():

    '''
    AKTYWNE NIEPARZYSTE 
    tu mamy kilka przypadków, ale jeśli istnieje choć jeden wiersz lub kolumna bez przycisku na pewno nie ma co rozpartywć nieparzystych.
    1. przekątne
    
    o - -    - - o    - o -    o - -
    - o -    - o -    - - o    - - o
    - - o    o - -    o - -    - o -

    - o - - 
    o - - - 
    - - o - 
    - - - o

    2. prostopadłe
    a. dla n nieparzystego

    o o o    o o o    - o -
    o - -    - o -    o o o
    o - -    - o -    - o -
    
    b. dla n parzystego

    - o o o    o - o o    - o - -
    o - - -    - o - -    o - o o
    o - - -    - o - -    - o - -
    o - - -    - o - -    - o - -
    '''
    jest = False
    '''jeśli w każdej kolumnie i w każdym wierszu jest donajmniej jeden przycisk zawsze da się zrobić nieparzystą ilość'''
    jest = len(np.argwhere(ilePrzyciskowWWierszu == 0)) == 0 and len(np.argwhere(ilePrzyciskowWKolumnie == 0)) == 0
    
    return jest

def zapiszPrzycisk(x,y):
    global przyciski, ilePrzyciskowWWierszu, ilePrzyciskowWKolumnie, przyciskiWWierszu, przyciskiWKolumnie, V
    przyciski[x-1,y-1] = 1
    # if przyciskiWWierszu[x-1] < 2:
    ilePrzyciskowWWierszu[x-1] += 1
    # if przyciskiWKolumnie[y-1] < 2:
    ilePrzyciskowWKolumnie[y-1] += 1
    
    if przyciskiWWierszu[x-1] is None:
        przyciskiWWierszu[x-1] = []
    przyciskiWWierszu[x-1].append(V)
    if przyciskiWKolumnie[y-1] is None:
        przyciskiWKolumnie[y-1] = []
    przyciskiWKolumnie[y-1].append(V)
    
    V += 1
    
def zaladujTablice(lines):
    global przyciski, ilePrzyciskowWWierszu, ilePrzyciskowWKolumnie, przyciskiWWierszu, przyciskiWKolumnie
    
    jest = False

    przyciski = np.zeros((n,n), np.int8)
    
    #do zastanowienia czy trzeba zwiększać tą ilość jeśli jest już 2
    ilePrzyciskowWWierszu = np.zeros((n), np.int32)
    ilePrzyciskowWKolumnie = np.zeros((n), np.int32)
    
    przyciskiWWierszu = np.empty((n), dtype=list)
    przyciskiWKolumnie = np.empty((n), dtype=list)
    for l in lines:
        x, y  = map(int,l.split(" "))
        zapiszPrzycisk(x,y)
    
    if not jest:
        jest = daSieAktywowacNieparzyste()
    
    if not jest:
        jest = daSieAktywowacParzyste()

    if jest:
        print("TAK")
    else:
        print("NIE")
    

sys.setrecursionlimit(100000)
# print(sys.getrecursionlimit())
                
wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("%s/testy/in/prz25.in"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz0.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz2ocen.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz3ocen.in')
# print("n: %i, m: %i"%(n,m))
# print(przyciski)


# print(arr)
# print("wolnePasy: %s\nodcinki: %s"%(wolnePasy, odcinki))


