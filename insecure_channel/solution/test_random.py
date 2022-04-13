seed = 0x1337

def srand(s):
    global seed
    seed = s % (2 ** 31)

def rand():
    global seed
    seed = (0x10001 * seed) % (2 ** 31)
    return seed

srand(1649431492)
first = rand()
second = rand()
iters = 0
while True:
    iters += 2
    r1 = rand()
    r2 = rand()
    if r1 == first and r2 == second:
        print(f'DONE in {iters} iters')
        break
