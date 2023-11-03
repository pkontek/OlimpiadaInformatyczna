import sys
import numpy as np
import pathlib
import itertools

n,m = 0,0
przyciski = []
wierszeZDwomaPrzyciskami = []
przekatne = []

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

def daSieAktywowacParzyste(wiersz):
    global wierszeZDwomaPrzyciskami
    
    '''
    
    AKTYWNE PARZYSTE 
    aktywowanie parzystych przycisków będzie możliwe tylko jeśli istnieją przyciski co najmniej 2 przyciski w jednym rzędzie mające swój odpowiednik w drugim rzędzie. Np.:
    o o -    o - - o    - - - -  
    - - -    - - - -    - o o -
    o o -    o - - o    - o o -
             - - - -    - - - -
    
    '''
    jest = False
    if np.sum(przyciski[wiersz]) > 1:
        for w in wierszeZDwomaPrzyciskami:
            a = np.array([przyciski[w],przyciski[wiersz]])
            if len(np.where(np.sum(a,0)>=2)[0]) > 1:
                jest = True
                break
        
        wierszeZDwomaPrzyciskami.append(wiersz)
    return jest

def daSieAktywowacNieparzyste():

    '''
    AKTYWNE NIEPARZYSTE 
    tu mamy kilka przypadków, ale jeśli istnieje choć jeden wiersz lub kolumna bez przycisku na pewno nie ma co rozpartywć nieparzystych.
    1. przekątne
    
    o - -    - - o    - o -    o - -
    - o -    - o -    - - o    - - o
    - - o    o - -    o - -    - o -

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
    
    jest = len(np.argwhere(przekatne == n)) > 0
            
    return jest

def sumujPrzekatne(x,y):
    global przekatne
    
    przekatne[0,y-x if y>=x else n + y - x ] += 1
    przekatne[1,(x + y - n if x+y >n else x+y) - 1] += 1
    

def zaladujTablice(lines):
    global przyciski, przekatne
    
    jest = False

    przyciski = np.zeros((n,n), np.int8)
    przekatne = np.zeros((2,n), np.int8)
    
    popx = 1
    for l in lines:
        x, y  = map(int,l.split(" "))
        przyciski[x-1,y-1] = 1
        sumujPrzekatne(x,y)
        if x > popx:
            if daSieAktywowacParzyste(popx-1):
                jest = True
                break
            popx = x
    
    if not jest:
        jest = daSieAktywowacParzyste(x-1)

    if not jest:
        jest = daSieAktywowacNieparzyste()
    
    if jest:
        print("TAK")
    else:
        print("NIE")
    


                
# wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz0.in')
wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz3ocen.in')
# print("n: %i, m: %i"%(n,m))
# print(przyciski)


# print(arr)
# print("wolnePasy: %s\nodcinki: %s"%(wolnePasy, odcinki))

