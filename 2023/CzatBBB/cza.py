import sys
#import numpy as np
import pathlib

n, k, a, b = 0, 0, 0, 0
s = ""
wynik = ""
wyst = {}


def wczytajDaneZPliku(path):
    global n, k, a, b, s
    input = open(path, 'r')
    n, k, a, b = map(int,input.readline().split(" "))
    
    s = input.readline().rstrip()
    input.close()

def wczytajDaneZStdin():
    global n, k, a, b, s
    input = sys.stdin
    n, k, a, b = map(int,input.readline().split(" "))
    
    s = input.readline().rstrip()
    

def dopiszR(r):
    global wyst
    r1 = r[0:k]
    r2 = r[k:k + 1]

    if r1 in wyst.keys():
        if r2 in wyst[r1]:
            wyst[r1][r2] += 1
        else:
            wyst[r1][r2] = 1
    else:
        wyst[r1] = {r2: 1}


def analizujWejscie():
    for i in range(0,n-k):
        r = s[i:i + k + 1]
        # print(r)
        dopiszR(r)
    # print(wyst)
    
def tworzSlowo():
    global s, wynik
    uzyte = []
    '''jeśli ponownie użyjemy tego samego prefiksu do dalszego tworzenia słowa mamy już cykl'''
    cyklStart = 0
    for i in range(b-n):
        r = s[-k:]
        znak = "a"
        ile = 0
        if r in uzyte:
            cyklStart = uzyte.index(r) 
            break
        uzyte.append(r)    
        if r in wyst:
            for z in wyst[r].keys():
                if ile < wyst[r][z]:
                    znak = z
                    ile = wyst[r][z]
                if ile == wyst[r][z] and z < znak:
                    znak = z
        s += znak
        # dopiszR(r+znak)
    # print(s)
    cykl = s[n + cyklStart:]
    przedCykl = s[n:n + cyklStart]
    # print(przedCykl, cykl)
    '''być może a zaczyna sie w środku cyku trzeb to dopisać'''
    if (a-n <= cyklStart):
        wynik = przedCykl[a-n-1:]
    else:
        wynik = cykl[(a-n-cyklStart)%len(cykl)-1:] 
    # print(wynik)
    '''dopisujemy cylkle o jeden więcej, bo może konczyć się w środku cyklu'''
    wynik += (cykl*(1+int((b-a)/len(cykl))))
    # print(wynik)
    '''obcinamy wynik aby zawierał tylko znaki od a do b'''
    wynik = wynik[:b-a+1] 
    

# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("%s/testy/in/cza1.in"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("2023/tester-oi-main/ocen/in/cza1ocen.in")

# print("n: %i, k: %i, a: %i, b: %i"%(n, k, a, b))
# print("s: '%s'"%s)
#    Received: cbcacbaadaadaadaadaadaadaadaadaadaadaadaadaadaadaad
#    Expected: cbaadaadaadaadaadaadaadaadaadaadaadaadaadaadaadaada

wczytajDaneZStdin()
analizujWejscie()
# print("mam mapę")
tworzSlowo()
# print(s)
print(wynik)
