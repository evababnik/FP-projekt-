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
            k[d][s]= float("-inf")
    k[0][0] = 0

    g = matrika(lamda,c)
    for d in range(c + 1):
        for s in range(lamda + 1):
            g[d][s]= float("-inf")
    g[0][0] = 0

    števec = 0
    # stevilo_predmetov_s_povecano_tezo = 0 
    for j in range(len(N)): # izberemo j-ti predmet 
        for d in range(c, w[j]-1, -1):  # in ga poskusimo dodati v svoji nominalni teži 
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]:
                z[d][lamda] = z[d - w[j]][lamda] + p[j] 
                k[d][lamda] = 1 + k[d - w[j]][lamda]
                if j + 1 > ((len(N) / 2)):
                    g[d][lamda] = 1 + g[d - w[j]][lamda]
                      
        for s in range(lamda, 0, -1): # poskusimo ga dodati v svoji robustni teži
            for d in range(c, maks_w[j] - 1, -1):
                if z[d - maks_w[j]][s - 1] + p[j] > z[d][s]:
                    z[d][s] = z[d - maks_w[j]][s - 1] + p[j]
                    k[d][s] = 1 + k[d - maks_w[j]][s-1]            

    z_zvedica = max([max(l) for l in z])
    pozicija = [[index, vrstica.index(z_zvedica)] for index, vrstica in enumerate(z) if z_zvedica in vrstica]
    c_zvezdica = pozicija[0][0] 
    #stevilo_predmetov_s_povecano_tezo = pozicija[-1][-1] 
    g_zvezdica = max(max(l) for l in g)
    k_zvezdica =  max(max(l) for l in k)
    # print(g_zvezdica)
    # if g_zvezdica < 0:
    #     g_zvezdica = 0
    # if k_zvezdica < 0:
    #     k_zvezdica = 0
    # if k_zvezdica - g_zvezdica < 0:
    #     k_zvezdica = 0
    # else: 
    #     k_zvezdica = k_zvezdica - g_zvezdica
    
    # indeks = k.index([največje_število])
    # k_zvezdica = k[indeks][lamda] - števec
    #k_zvezdica = k[c_zvezdica][stevilo_predmetov_s_povecano_tezo]
    return (z_zvedica, c_zvezdica, k_zvezdica)


# primer:
# print(RKP({1,2,3,4,5}, 15, [2,2,3,4,5], [4, 5, 6, 4, 2], 2, [4, 4, 3, 6, 6]))
# print(RKP({1,2,3}, 7, [2,2,3], [4, 5, 6], 2, [4, 4, 3]))
# print(RKP({1,2,3,4,5,6,7,8,9,10,11,12}, 20, [2,2,3,40,5,2, 2,3,4,5, 1,14], [4, 5, 6, 4, 2, 4, 5, 6, 4, 2, 2,15]))
# RKP({1,2,3,4,5}, 17, [2,2,3,4,5], [4, 5, 6, 4, 2])
# RKP({1,2,3,4,5}, 4, [2,2,3,4,5], [4, 5, 6, 4, 2])



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
#print(RKP({1,2,3}, 2, 6, [2,2,3], [4, 5, 6], [40, 40, 50]))

#print(RKP({0,1, 2}, 2, 30 , [7, 4, 4], [10, 5, 4], [10, 8, 6]))
# primer:
# print(RKP({1,2,3,4,5, 6}, 2, 15, [2,2,3,4,5, 6], [4, 5, 6, 4, 2, 5], [4, 4, 3, 6, 6, 6]))



def rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p, c):
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
        a = int((n / 2 ))
        N1 = N[:a]
        N2 = N[a:]
        w1 = w[:a]
        w2 = w[a:] 
        maks_w1 = maks_w[a:]
        maks_w2 = maks_w[:a]
        p1 = p[:a]
        p2 = p[a:]
    
        if k_zvezdica >= lamda:
            z1_c_zvezdica = RKP(N1, lamda, c_zvezdica, w, p, maks_w)[0]
            z2_c_zvezdica = solve_KP(N2, c_zvezdica, w, p)[1] # tu ko boma dodala v RKP da naredi seznam še lahk kličema kr RKP
            for c_1 in range(c_zvezdica + 1):
                z1_c_1 = RKP(N1, c_zvezdica, w, p, lamda, maks_w)[0]
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w, p)[1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
            solution_set_kp = solve_KP(N2, z2_c2, w, p)[0]
            #k1_zvezdica
            rekurzija(N1, z1_c1, k1_zvezdica, c1,lamda, w, maks_w, p)        
        else: 
            z1_c_zvezdica = solve_eKkP(N1,c_zvezdica, maks_w, k_zvezdica,k_zvezdica)[1]
            z2_c_zvezdica = RKP(N2, c_zvezdica, w, p, lamda - k_zvezdica, maks_w)[0]
            for c_1 in range(c_zvezdica + 1):
                z1_c_1 = RKP(N1, c_zvezdica, w, p, lamda, maks_w)[0]
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w, p)[-1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
            solution_set_eKkP = solve_eKkP(z2_c2, c, w, p)[0]
            # k2_zvezdica 
            rekurzija(N1, z2_c2, k2_zvezdica, c2,lamda - k_zvezdica, w, maks_w, p)
