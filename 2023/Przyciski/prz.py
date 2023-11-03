import sys
import numpy as np
import pathlib
import itertools

n,m = 0,0
przyciski = []
wierszeZDwomaPrzyciskami = []
przyciskiWWierszu = []
przyciskiWKolumnie = []

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
    aktywowanie parzystych przycisków będzie możliwe tylko jeśli istnieją przyciski co najmniej 2 przyciski w jednym rzędzie mające swój odpowiednik w drugim rzędzie. Np.:
    o o -    o - - o    - - - -  
    - - -    - - - -    - o o -
    o o -    o - - o    - o o -
             - - - -    - - - -
    
    '''
    jest = False
    
    # wszystkie kombinacje wierszy z więcej niż jednym przyciskiem
    for wiersze in itertools.combinations(np.argwhere(przyciskiWWierszu == 2),2):
        w1,w2 = wiersze[0][0],wiersze[1][0]
        a = np.array([przyciski[w1],przyciski[w2]])
        if len(np.where(np.sum(a,0)>=2)[0]) > 1:
            jest = True
            break
        
    return jest

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
    jest = len(np.argwhere(przyciskiWWierszu == 0)) == 0 and len(np.argwhere(przyciskiWKolumnie == 0)) == 0
    
    return jest

def zapiszPrzycisk(x,y):
    global przyciski, przyciskiWWierszu, przyciskiWKolumnie
    przyciski[x-1,y-1] = 1
    if przyciskiWWierszu[x-1] < 2:
        przyciskiWWierszu[x-1] += 1
    if przyciskiWKolumnie[y-1] < 2:
        przyciskiWKolumnie[y-1] += 1
    
def zaladujTablice(lines):
    global przyciski, przyciskiWWierszu, przyciskiWKolumnie
    
    jest = False

    przyciski = np.zeros((n,n), np.int8)
    
    #do zastanowienia czy trzeba zwiększać tą ilość jeśli jest już 2
    przyciskiWWierszu = np.zeros((n), np.int8)
    przyciskiWKolumnie = np.zeros((n), np.int8)
    
    for l in lines:
        x, y  = map(int,l.split(" "))
        zapiszPrzycisk(x,y)
    
    if not jest:
        jest = daSieAktywowacParzyste()

    if not jest:
        jest = daSieAktywowacNieparzyste()
    
    if jest:
        print("TAK")
    else:
        print("NIE")
    


                
wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz0.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz3ocen.in')
# print("n: %i, m: %i"%(n,m))
# print(przyciski)


# print(arr)
# print("wolnePasy: %s\nodcinki: %s"%(wolnePasy, odcinki))

