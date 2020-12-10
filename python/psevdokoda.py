#Psevodokodi za solve_RKP in rekurzija

def solve_RKP(N, c, w, p, lamda = None,  max_w = None):
    # Najprej uredimo podatke po padajoči teži (max_w - w)
    # Če je max_w = None, uredimo podatke padajoče po teži (w)

    # Naredimo matrike Z, K, G in nastavimo začetne pogoje
    for d := 0 in range(c + 1): 
        for s in range(lamda + 1): 
            Z[d][s]= float("-inf")
    Z[0][0] = 0  # Element v prvi vrstici in prvem stolpcu matrike nastavimo na 0 vse ostale na minus neskončno
    # Analogno naredimo še matriki K in G

    for j in range(len(N)): # izberemo j-ti predmet 
        for d in range(c, w[j]-1, -1):  # in ga poskusimo dodati v nahrbtnik v svoji nominalni teži 
            if z[d - w[j]][lamda] + p[j] > z[d][lamda]: #pri pogoju, da smo že vstavili 
                z[d][lamda] = z[d - w[j]][lamda] + p[j]  #lamda predmetov
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

        z_zvedica = max([max(l) for l in z]) #tako dobimo max vrednost (največji element matrike z)
        pozicija = [[index, vrstica.index(z_zvedica)] for index, vrstica in enumerate(z) if z_zvedica in vrstica]
        c_zvezdica = pozicija[0][0] #vrstica in stolpec max vrednosti predstavljata skupno težo vstavljenih predmetov
        stevilo_predmetov_s_povecano_tezo = pozicija[0][-1] #in število predmetov, ki se jim spremeni teža
        g1 = g[c_zvezdica][stevilo_predmetov_s_povecano_tezo] #g1 se v g nahaja na istem mestu kot z_zvezdica(pomeni koliko elementov iz N2 je v optimalni rešitvi)
        k_zvezdica = k[c_zvezdica][stevilo_predmetov_s_povecano_tezo] #na istem mestu kot z_zvezdica se nahaja tudi število vseh vstavljenih predmetov v optimalni rešitvi
        g_zvezdica = k_zvezdica - g1 #g_zvezdica = št.elementov v N1, k_zvezdica = št. vseh elementov
        return [z_zvedica, c_zvezdica, k_zvezdica, g_zvezdica]
