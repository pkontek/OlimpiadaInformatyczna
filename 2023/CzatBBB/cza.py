import sys
import numpy as np
import pathlib

from typing import List

n, k, a, b = 0, 0, 0, 0
s = ""
wynik = ""
wyst = {}

base: int = 123
mod: int = 10**18 + 7
power = []

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

def nowyHash(current_hash, pop, add):
    new_hash = (current_hash - power[k - 1] * ord(pop)) % mod
    new_hash = (new_hash * base + ord(add)) % mod
    return new_hash

def dopiszR(r, h1):
    global wyst
    r2 = r[-1]

    if h1 in wyst.keys():
        if r2 in wyst[h1]:
            wyst[h1][r2] += 1
        else:
            wyst[h1][r2] = 1
    else:
        wyst[h1] = {r2: 1}

def analizujWejscie():
    global s, wynik, power
    
    hash_values = []
    
    current_hash = 0

    power = [1] * (k) #(n + 1)
 
    for i in range(1, k):
        power[i] = (power[i - 1] * base) % mod
 
    r = ""

    for i in range(k):
        current_hash = (current_hash * base + ord(s[i])) % mod
        r += s[i]
    
    # hash_values = [0] * (n - k + 1)

    #pierwszy hash do zapisania
    hash_values.append(current_hash)
 
    for i in range(1, n - k + 1):
        
        r += s[i + k - 1]
        
        current_hash = nowyHash(current_hash, r[0], r[-1])
 
        hash_values.append(current_hash)

        dopiszR(r, hash_values[i-1])
        
        r = r[1:]
        
    w = {}
    for h in wyst.keys():
        ile = 0
        for z in wyst[h].keys():
            if ile < wyst[h][z]:
                znak = z
                ile = wyst[h][z]
            if ile == wyst[h][z] and z < znak:
                znak = z
        w[h] = znak
    uzyte = []
    '''jeśli ponownie użyjemy tego samego prefiksu do dalszego tworzenia słowa mamy już cykl'''
    cyklStart = 0
    for i in range(b-n):
        znak = "a"
        ile = 0
        if current_hash in uzyte:
            cyklStart = uzyte.index(current_hash) 
            break
        uzyte.append(current_hash)
        if current_hash in w:
            znak = w[current_hash]
        r += znak
        current_hash = nowyHash(current_hash,r[i], znak)
        hash_values.append(current_hash)
        s += znak

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
wczytajDaneZPliku("%s/testy/in/cza3.in"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("2023/tester-oi-main/ocen/in/cza0.in")

print("n: %i, k: %i, a: %i, b: %i"%(n, k, a, b))
# print("s: '%s'"%s)
#    Received: cbcacbaadaadaadaadaadaadaadaadaadaadaadaadaadaadaad
#    Expected: cbaadaadaadaadaadaadaadaadaadaadaadaadaadaadaadaada



# wczytajDaneZStdin()


analizujWejscie()
# # print(s)
print(wynik)
