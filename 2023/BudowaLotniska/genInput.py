import random
n = 30
output = open('input.txt', 'w')
output.write("%d"%n)

for i in range(n):
    output.write("\n")
    for j in range(n):
        output.write(random.choices([".","X"],[3,1])[0])

output.close()