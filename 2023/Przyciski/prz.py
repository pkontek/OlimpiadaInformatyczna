import sys
import numpy as np
import pathlib
import itertools

n,m = 0,0
przyciskiWWierszu = []
przyciskiWKolumnie = []
stos = []
przyciski = []
V = 0
graf = dict()
wierzcholki = set()

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

def dodajDoGrafu(graf, w1, w2):
    if w1 not in graf:
        graf.update({w1 : [w2]})
    else:
        graf[w1].append(w2)
    if w2 not in graf:
        graf.update({w2 : [w1]})
    else:
        graf[w2].append(w1)

def zbadajGraf(graf):
    global ileWierzch, wiersz, kolumna, wierzcholki
    visited = [False]*(n*2)
    parzystaIlWierzch = True;

    wynik = set()

    for i in range(n*2):
        # Don't recur for u if it
        # is already visited
        if visited[i] == False:
            ileWierzch = 1
            wiersz = -1
            kolumna = -1
            wierzcholki = set()

            if(isCyclicUtil(graf, i, visited, -1)) == True:
                #jest cykl - czyli da się osiągnąć parzyste - wynik jest na stosie
                wiersz = -1
                kolumna = -1
                wynik = set()

                for i in stos:

                    if i<n:
                        wiersz = i
                    else:
                        kolumna = i-n
                    if wiersz >=0 and kolumna >=0:
                        wynik.add((wiersz,kolumna))

                return True, wynik
            parzystaIlWierzch = parzystaIlWierzch and ileWierzch%2 == 0
            wynik.update(wierzcholki)
    #nie znaleziono cyklu, ale jeśli w każdym spójnym podgrafie jest parzysta ilość wierzchołków, to da się osiągnąć nieparzyste
    return parzystaIlWierzch, wynik

def isCyclicUtil(graf, v, visited, parent):
    global ileWierzch, wiersz, kolumna, wierzcholki

    visited[v] = True
    stos.append(v)
    
    if v<n:
        wiersz = v
    else:
        kolumna = v-n
    
    # if wiersz >= 0 and kolumna >=0:
    #     print((wiersz,kolumna))
    #jeśli węzła nie ma w grafie - to znaczy że nie ma powiązań z innymi
    if v in graf.keys():

        # Recur for all the vertices
        # adjacent to this vertex
        for i in graf[v]:
            # If the node is not
            # visited then recurse on it
            if i<n:
                wiersz = i
            else:
                kolumna = i-n
            wierzcholki.add((wiersz,kolumna))
            if visited[i] == False:
                ileWierzch += 1
                if(isCyclicUtil(graf, i, visited, v)):
                    return True
            # If an adjacent vertex is
            # visited and not parent
            # of current vertex,
            # then there is a cycle
            elif parent != i:
                
                stos.append(i)
                return True
    stos.pop()
    return False

def zapiszPrzycisk(x,y):
    global przyciski, przyciskiWWierszu, przyciskiWKolumnie, V, graf
    
    
    przyciski.append((x-1, y-1))
    if przyciskiWWierszu[x-1] is None:
        przyciskiWWierszu[x-1] = []
    przyciskiWWierszu[x-1].append(V)
    if przyciskiWKolumnie[y-1] is None:
        przyciskiWKolumnie[y-1] = []
    przyciskiWKolumnie[y-1].append(V)
    
    #wiersze zaczynają się od 0 a kolumny od n
    dodajDoGrafu(graf, (x-1), n+(y-1))

    V += 1
    
def zaladujTablice(lines):
    global przyciskiWWierszu, przyciskiWKolumnie
    
    jest = False
    
    przyciskiWWierszu = np.empty((n), dtype=list)
    przyciskiWKolumnie = np.empty((n), dtype=list)
    for l in lines:
        x, y  = map(int,l.split(" "))
        zapiszPrzycisk(x,y)
    jest, wynik = zbadajGraf(graf)
    
    if jest:
        print("TAK")
        if wynik != []:
            print(len(wynik))
            for p in wynik:
                print(przyciski.index(p) + 1, end = " ")
        print()
    else:
        print("NIE")

sys.setrecursionlimit(1000000)
                
wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("%s/testy/in/prz25.in"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz0.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz1ocen.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz2ocen.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz3ocen.in')
# print("n: %i, m: %i"%(n,m))
# print(przyciski)




