"""
Robustni Problem Nahrbtinka
"""

def matrika(m,n):
    return [[0] * (m+1) for _ in range(n+1)]

def podatki(w, p, maks_w = None):
    if maks_w is None:
         vrstni_red = [i[0] for i in sorted(enumerate(w), key=lambda x:x[1])]
         w = [w[i] for i in vrstni_red]
         p = [p[i] for i in vrstni_red]
         return (w[::-1], p[::-1])
    else:  
        urejen_sez = [0] * len(maks_w)
        for i in range(len(maks_w)):
            urejen_sez[i] = maks_w[i] - w[i]
        vrstni_red = [i[0] for i in sorted(enumerate(urejen_sez), key=lambda x:x[1])]
        maks_w = [maks_w[i] for i in vrstni_red]
        p = [p[i] for i in vrstni_red]
        w = [w[i] for i in vrstni_red]
        return (w[::-1], p[::-1], maks_w[::-1])



# primer
# print(podatki([20,19,18,17,16,15,14],[20,10,14,13,11,2,24],[10,10,10,10,10,10,10]))

def particija(N):
    n = len(N)
    N1 = []
    N2 = []
    for el in N:
        if N.index(el) < (n / 2):
            N1.append(el)
        else:
            N2.append(el)
    return N1, N2

def RKP(N, c, w, p, lamda = None,  maks_w = None):
    # uporabiva funkcijo podatki, ki podatke spremeni v pravo obliko
    if maks_w is not None:
        pravilni_podatki = podatki(w, p, maks_w)
        w, p, maks_w = pravilni_podatki[0], pravilni_podatki[1], pravilni_podatki[2]
        print(w)
        print(p)
    else: 
        pravilni_podatki = podatki(w, p)
        w, p = pravilni_podatki[0], pravilni_podatki[1]
        print(w)
        print(p)
        pass
    if lamda is not None:
        if lamda > len(N):
            raise ValueError("Lamda je večja kot moč množice predmetov")
    if lamda == None or 0:
        maks_w = [c]* len(w)
        lamda = 0
    if c < min(w):
        return 0
    if len(N) == len(w) == len(p) == len(maks_w): 
        pass
    else: 
        raise ValueError("Napačno vneseni podatki")

    z = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            z[d][s]= float("-inf")
    z[0][0] = 0
    c_zvezdica = 0

    k = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            k[d][s]= 0
    k[0][0] = 0

    g = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            g[d][s] = 0
    g[0][0] = 0

    # stevilo_predmetov_s_povecano_tezo = 0 
    for j in range(len(N)): # izberemo j-ti predmet 
        for d in range(c, w[j]-1, -1):  # in ga poskusimo dodati v svoji nominalni teži 
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]:
                z[d][lamda] = z[d - w[j]][lamda] + p[j] 
                k[d][lamda] = 1 + k[d - w[j]][lamda]
                if j  >= ((len(N) / 2)):
                    g[d][lamda] = 1 + g[d - w[j]][lamda]
                      
        for s in range(lamda, 0, -1): # poskusimo ga dodati v svoji robustni teži
            for d in range(c, maks_w[j] - 1, -1):
                if z[d - maks_w[j]][s - 1] + p[j] > z[d][s]:
                    z[d][s] = z[d - maks_w[j]][s - 1] + p[j]
                    k[d][s] = 1 + k[d - maks_w[j]][s-1] 
                    if j  >= ((len(N) / 2)):
                        g[d][s] = 1 + g[d - maks_w[j]][s - 1]


    z_zvedica = max([max(l) for l in z])
    pozicija = [[index, vrstica.index(z_zvedica)] for index, vrstica in enumerate(z) if z_zvedica in vrstica]
    c_zvezdica = pozicija[0][0] 
    stevilo_predmetov_s_povecano_tezo = pozicija[-1][-1] 
    g1 = g[c_zvezdica][stevilo_predmetov_s_povecano_tezo]
    k_zvezdica = k[c_zvezdica][stevilo_predmetov_s_povecano_tezo]
    g_zvezdica = k_zvezdica - g1 #g_zvezdica = št.elementov v N1, k_zvezdica = št. vseh elementov
    
    return (z_zvedica, c_zvezdica, k_zvezdica, g_zvezdica)

# primer:
# print(RKP({1,2,3}, 7, [2,2,3], [4, 5, 6], 2, [4, 4, 3]))
# print(RKP({1,2,3,4,5,6,7,8,9,10,11,12}, 20, [2,2,3,40,5,2, 2,3,4,5, 1,14], [4, 5, 6, 4, 2, 4, 5, 6, 4, 2, 2,15]))
# RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])
# RKP({1,2,3,4,5,6}, 6, [1,1,1,2,3,9])


def solve_KP(N, c, w, p):  
    n = len(N)
    z = matrika(c, n)
    for j in range(n + 1): 
        for d in range(c + 1): 
            if j == 0 or d == 0: 
                z[j][d] = 0
            elif w[j-1] <= d: 
                z[j][d] = max(p[j-1] + z[j-1][d-w[j-1]], z[j-1][d]) 
                z[j][d] == p[j-1] + z[j-1][d-w[j-1]]
            else: 
                z[j][d] = z[j-1][d] 
    z_zvezdica = [n][c]
    z_zvezdica1 = [n][c]
    c_zvezdica = 0
    c_zvezdica = 0
    seznam_stvari = []
    for i in range(n, 0, -1):
        if z_zvezdica1 <= 0:
            break
        if z_zvezdica1 == z[i - 1][c]:
            continue
        else:
            seznam_stvari.append([i, w[i - 1], p[i - 1]])
            c_zvezdica += w[i - 1]
            z_zvezdica1 -= p[i - 1]
            c -= w[i - 1]
    return [seznam_stvari, z_zvezdica]


def solve_eKkP(N, c, w, p, k):
    n = len(N)
    z = [[[0 for col in range(k + 1)] for col in range(c + 1)] for row in range(n + 1)]
    for j in range(n + 1): 
        for d in range(c + 1):
            for m in range(k + 1): 
                if j == 0 or d == 0 or m == 0: 
                    z[j][d][m] = 0
                elif w[j-1] <= d: 
                    z[j][d][m] = max(p[j-1] + z[j-1][d-w[j-1]][m - 1], z[j-1][d][m])         
                else: 
                    z[j][d][m]= z[j-1][d][m]
    z_zvezdica = z[n][c][k]
    z_zvezdica1 = z[n][c][k]
    c_zvezdica = 0
    seznam_stvari = []
    for i in range(n, 0, -1):
        if z_zvezdica1 <= 0:
            break
        elif z_zvezdica1 == z[i - 1][c][k]:
            continue
        else:
            seznam_stvari.append([i, w[i - 1], p[i - 1]])
            c_zvezdica += w[i - 1]
            z_zvezdica1 -= p[i - 1]
            c -= w[i - 1]
    return([seznam_stvari, z_zvezdica])

# primer
#print(solve_eKkP([1, 2, 3, 4], 10,[2, 3, 6, 4], [1, 2, 5, 3], 2))
#print(solve_eKkP([1, 2, 3, 4], 10,[2, 3, 6, 4], [1, 2, 5, 3], 2))


def rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p):
    if len(N) == 1:
        if lamda != 0:
            if maks_w[0] <= c_zvezdica:
                return N
            else:
                print("V nahrbtnik ne moremo dati nobene stvari.")
        else:
            if w[0] <= c_zvezdica:
                return N
            else:
                print(" V nahrbtnik ne moremo dati nobene stvari.")
    else:
        n = len(N)  #N razdelimo na N1 in N2
        polovica = int((n / 2 ))
        N1 = N[:polovica]
        N2 = N[polovica:]
        w1 = w[:polovica]
        w2 = w[polovica:] 
        maks_w1 = maks_w[polovica:]
        maks_w2 = maks_w[:polovica]
        p1 = p[:polovica]
        p2 = p[polovica:]
    
        if k_zvezdica >= lamda:
            z1_c_zvezdica = RKP(N1, c_zvezdica, w1, p1, lamda, maks_w1)[0]
            z2_c_zvezdica = solve_KP(N2, c_zvezdica, w2, p2)[1] # tu ko boma dodala v RKP da naredi seznam še lahk kličema kr RKP
            for c_1 in range(c_zvezdica + 1):
                z1_c_1 = RKP(N1, c_1, w1, p1, lamda, maks_w1)[0]
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w2, p2)[1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
                    solution_set_kp = solve_KP(N2, z2_c2, w2, p2)
                k1_zvezdica = RKP(N1, z1_c1, w1, p1, lamda, maks_w1)[3]
                rekurzija(N1, z1_c1 , k1_zvezdica, c1, lamda, w1, maks_w1, p1)        
        else: 
            z1_c_zvezdica = solve_eKkP(N1, c_zvezdica, maks_w1, p1, k_zvezdica)[1]
            z2_c_zvezdica = RKP(N2, c_zvezdica,w2, p2, lamda - k_zvezdica, maks_w2)[0]
            for c_1 in range(c_zvezdica + 1):
                z1_c_1 = RKP(N1, c_1, w1, p1, lamda, maks_w1)[0]
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w2, p2)[1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
                solution_set_eKkP = solve_eKkP(N2, z2_c2, w, p, k_zvezdica)[0]
                k2_zvezdica = RKP(N1, z2_c2, w1, p1, lamda, maks_w1)[3]
                rekurzija(N2, z2_c2, k2_zvezdica, c_zvezdica,lamda - k_zvezdica, w, maks_w, p)
