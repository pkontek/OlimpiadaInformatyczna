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
    global przyciski, przyciskiWKolumnie, przyciskiWWierszu
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

    Aby określić czy mamy możliwość zapalić parzyste trzeba usunąć pojedyncze przyciski z wiersza i wykluczyć wiersze zerowe. jeśli pozostaną co najmniej 2 wiersze i 2 kolumny z przyciskami, możan będzie właczyć tak aby zapewnić parzystość.

    '''
    jest = False
    # print("przyciski: \n%s"%przyciski)
    # print("przyciskiWWierszu: %s"%przyciskiWWierszu)
    # print("przyciskiWKolumnie: %s"%przyciskiWKolumnie)
    
    jedynkiWWierszach = np.argwhere(przyciskiWWierszu==1)
    jedynkiWKolunach  = np.argwhere(przyciskiWKolumnie==1)

    while (len(jedynkiWWierszach) + len(jedynkiWKolunach)) > 0:
        if len(jedynkiWWierszach) > 0:
            wiersz = jedynkiWWierszach[0][0]
            kolumna = np.argwhere(przyciski[wiersz]==1)[0][0]
        else:
            kolumna = jedynkiWKolunach[0][0]
            wiersz = np.argwhere(przyciski.T[kolumna]==1)[0][0]
        przyciski[wiersz, kolumna] = 0
        przyciskiWWierszu[wiersz] -= 1
        przyciskiWKolumnie[kolumna] -= 1
        jedynkiWWierszach = np.argwhere(przyciskiWWierszu==1)
        jedynkiWKolunach  = np.argwhere(przyciskiWKolumnie==1)
    
    if len(np.argwhere(przyciskiWWierszu>1)) >1 and len(np.argwhere(przyciskiWKolumnie>1))>1:
        jest = True

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
    # if przyciskiWWierszu[x-1] < 2:
    przyciskiWWierszu[x-1] += 1
    # if przyciskiWKolumnie[y-1] < 2:
    przyciskiWKolumnie[y-1] += 1
    
def zaladujTablice(lines):
    global przyciski, przyciskiWWierszu, przyciskiWKolumnie
    
    jest = False

    przyciski = np.zeros((n,n), np.int8)
    
    #do zastanowienia czy trzeba zwiększać tą ilość jeśli jest już 2
    przyciskiWWierszu = np.zeros((n), np.int32)
    przyciskiWKolumnie = np.zeros((n), np.int32)
    
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
    


                
wczytajDaneZStdin()
# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("%s/testy/in/prz23.in"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz0.in')
# wczytajDaneZPliku('2023/tester-oi-main/ocen/in/prz3ocen.in')
# print("n: %i, m: %i"%(n,m))
# print(przyciski)


# print(arr)
# print("wolnePasy: %s\nodcinki: %s"%(wolnePasy, odcinki))

