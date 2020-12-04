"""
Robustni Problem Nahrbtinka
"""

def matrika(m,n):
    return [[0] * (m+1) for _ in range(n+1)]


def RKP(N, lamda, c, w, p, maks_w):
    z = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            z[d][s]= float("-inf")
    z[0][0] = 0
    c_zvezdica = 0
    stevilo_predmetov_s_povecano_tezo = 0
    for j in range(len(N)):
        for d in range(c, w[j]-1, -1):
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]:
                z[d][lamda] = z[d - w[j]][lamda] + p[j]
                         
        for s in range(lamda, 0, -1):
            for d in range(c, maks_w[j] - 1, -1):
                if z[d - maks_w[j]][s - 1] + p[j] > z[d][s]:
                    z[d][s] = z[d - maks_w[j]][s - 1] + p[j]               
                                     
    z_zvedica = max([max(l) for l in z])
    pozicija = [[index, vrstica.index(z_zvedica)] for index, vrstica in enumerate(z) if z_zvedica in vrstica]
    c_zvezdica = pozicija[0][0] 
    stevilo_predmetov_s_povecano_tezo = pozicija[-1][-1] 
    print(z)
    return (z_zvedica, c_zvezdica)



def solve_KP(N, c, w, p, k):  
    n = len(N)
    z = matrika(c, n)
    k = 0
    for j in range(n + 1): 
        for d in range(c + 1): 
            if j == 0 or d == 0: 
                z[j][d] = 0
            elif w[j-1] <= d: 
                z[j][d] = max(p[j-1] + z[j-1][d-w[j-1]], z[j-1][d])

            else: 
                z[j][d] = z[j-1][d] 
    return z[n][c] 

#print(RKP({1,2,3}, 1, 6, [2,2,3], [4, 5, 6], [40, 40, 50]))

print(RKP({0,1, 2}, 2, 30 , [7, 4, 4], [10, 5, 4], [10, 8, 6]))
# primer:
# print(RKP({1,2,3,4,5}, 2, 15, [2,2,3,4,5], [4, 5, 6, 4, 2], [4, 4, 3, 6, 6]))
