import random

def naredi_podatke(n, c, gama, max_cena): #funkcija zgenerira naključne podatke
    
    #n = random.randint(1, stevilo)
    #c = random.randint(0, teza)
    #gama = random.randint(0, int(n / 3))
    N = []
    w = []
    maks_w = []
    p = []
    for i in range(1, n + 1):
        N.append(i)
    for i in range(1, n + 1):
        nominal_w = random.randint(0, c)
        w.append(nominal_w)
    for i in range(1, n + 1):
            nominal_w = w[i - 1]
            max_w = random.randint(nominal_w, nominal_w + 20)
            maks_w.append(max_w)
    for i in range(1, n + 1):
        val = random.randint(0, max_cena + 1)
        p.append(val)
    with open("%s" % n +'-' "%s" % c + '-' "%s.txt" % gama, 'w', encoding='utf-8') as izhodna:
        for i in range(len(N)):
            izhodna.write("{} {} {} {}\n".format(N[i], p[i], w[i], maks_w[i]))

    return [N, c, w, p, gama, maks_w]

print(naredi_podatke(2000, 50, 1, 100))
