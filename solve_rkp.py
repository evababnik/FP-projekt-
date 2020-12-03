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

    for j in range(len(N)):
        for d in range(c, w[j]-1, -1):
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]:
                z[d][lamda] = z[d - w[j]][lamda] + p[j]
        for s in range(lamda, 0, -1):
            for d in range(c, maks_w[j] - 1, -1):
                if z[d - maks_w[j]][s - 1] + p[j] > z[d][s]:
                    z[d][s] = z[d - maks_w[j]][s - 1] + p[j]
    z_zvedica = max([max(l) for l in z])
    print(z)
    return (z_zvedica)

def solve_KP(N, c, w, p):  
    n = len(N)
    z = matrika(c, n)
    for j in range(n + 1): 
        for d in range(c + 1): 
            if j == 0 or d == 0: 
                z[j][d] = 0
            elif w[j-1] <= d: 
                z[j][d] = max(p[j-1] + z[j-1][d-w[j-1]],  z[j-1][d]) 
            else: 
                z[j][d] = z[j-1][d] 
    return z[n][c] 


#RKP({1,2,3}, 2, 6, [2,2,3], [4, 5, 6], [40, 40, 50])
