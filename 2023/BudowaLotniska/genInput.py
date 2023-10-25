import random, pathlib
n = 5
m = 2
output = open("%s/input.txt"%pathlib.Path(__file__).parent.resolve(), 'w')
output.write("%d %d"%(n,m))

for i in range(n):
    output.write("\n")
    for j in range(n):
        output.write(random.choices([".","X"],[3,1])[0])

output.close()