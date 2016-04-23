f = open('input_all.txt')
c = 0
for line in f:
	c += 1
print('Input: ' + str(c))
f.close()

f = open('output.txt')
c = 0
for line in f:
        c += 1
print('Output: ' + str(c))
f.close()
