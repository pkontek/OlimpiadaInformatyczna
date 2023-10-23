import random
n = 1500
m = 2
output = open('input.txt', 'w')
output.write("%d %d"%(n,m))

for i in range(n):
    output.write("\n")
    for j in range(n):
        output.write(random.choices([".","X"],[3,1])[0])

output.close()