import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

for i in range(2):
    print('i = ', i)

print("testing")

sys.stdout = orig_stdout
f.close()
