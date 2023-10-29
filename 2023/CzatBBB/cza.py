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
        dopiszR(r)
    
def tworzSlowo():
    global s, wynik
    for i in range(b-n):
        r = s[-k:n+i]
        znak = "a"
        ile = 0
        if r in wyst.keys():
            for z in wyst[r].keys():
                if ile < wyst[r][z]:
                    znak = z
                    ile = wyst[r][z]

        s += znak
        dopiszR(r+znak)


# wczytajDaneZPliku("%s/input.txt"%pathlib.Path(__file__).parent.resolve())
# wczytajDaneZPliku("2023/tester-oi-main/ocen/in/cza3ocen.in")

# print("n: %i, k: %i, a: %i, b: %i"%(n, k, a, b))
# print("s: '%s'"%s)

wczytajDaneZStdin()
analizujWejscie()
tworzSlowo()

print(s[-(b+1-a):])