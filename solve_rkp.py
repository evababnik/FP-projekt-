"""
Robustni problem nahrbtinka
"""

def matrika(m,n):
    return [[0] * (m+1) for _ in range(n+1)]


def RKP(N, lamda, c, w, p, maks_w):
    z = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            z[d][s]= float("-inf")
    z[0][0] = 0

    for j in range(len(N)):
        for d in range(c, w[j]-1, -1): # prva zanka
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]:
                z[d][lamda] = z[d - w[j]][lamda] + p[j]
        for s in range(lamda, 0, -1):
            for d in range(c, maks_w[j] - 1, -1):
                if z[d - maks_w[j]][s - 1] + p[j] > z[d][s]:
                    z[d][s] = z[d - maks_w[j]][s - 1] + p[j]
    z_zvedica = max([max(l) for l in z])
    print(z)
    return (z_zvedica)



#Gre za robustni problem nahrbtnika, torej zanima nas katere predmete naj pospravimo v nahbrtnik 
# ki imajo teže W[j] in vrednost p[j] na tak način da bomo dobili čimvečjo vrednost. Ampak od teh
# predmetov jih lahko največ gamma predmetov spremeni svojo težo na maks_w[j] (torej da nimamo točnih podatkov npr.) in je 
# težava če imajo večjo težo, pač to je potrebno upoštevat pri iskanju optimalne reštive. Midva sva kodo 
# spremenila iz psevdokode v pythonovo obliko in seveda uredila indekse in vse potrebno ampak koda ne dela 
# in se nama tudi ne zdi smiselna. Za enih par primerov sem si na roko izpisal vse kar koda naredi,
# in pride do čistega nesmisla v prvi zanki, saj se rezultat nikoli ne more spremeniti ker je vedno 
# - neskončno. Upam da boste razumeli v čem je problem, saj midva sumiva da je koda napačna ali pa 
# sva se nekje zmotila, ampak te napake nikakor ne najdeva. 
# spodaj imate tudi primer, ki sem ga na roke izpisal in vrne napačno vrednost, kot zanimivost 
# sem ugotovil tudi da lahko teže spreminjam na poljubne vrednosti npr 200 in koda vedno vrne isti 
# rezultat


#print(RKP({1,2,3}, 2, 20, [200, 190, 200], [10, 30, 50], [10, 8, 7]))
print(RKP({1,2,3}, 2, 6, [2,2,3], [4, 5, 6], [4, 4, 5]))
# N = {1,2,3}, lamda = 2, c = 10, w = [5,6,4], p = [15,20,16]
# maks_w = [6,6,6]

#RKP({1,2,3}, 2, 6, [2,2,3], [4, 5, 6], [40, 40, 50])
