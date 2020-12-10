Psevodokodi za solve_RKP in rekurzija 

def solve_RKP(N, c, w, p, lamda = None,  max_w = None):
    # slovar predmetov spremenimo v resitev predmetov
    N = v_seznam(N)
    if len(N) == 1:
        if lamda != 0:
            if maks_w[0] <= c: #če imamo samo en element, ki spremeni svojo težo na maks_w <= c,
                return [p[0], maks_w[0], 1, 0]  #je to edini element, ki ga damo v nahrbtnik 
            else:
                return [0, 0, 0, 0]  
        else:
            if w[0] <= c:
                return [p[0], w[0], 1, 0] #če predmet ne spremeni svoje teže, ga dodamo v nahrbnik,
            else:                          #če je w <= c
                return [0, 0, 0, 0]
    else:
        if maks_w is not None:
            pravilni_podatki = podatki(N, w, p, maks_w) #uporabiva funkcijo podatki, ki podatke spremeni v pravo obliko
            N, w, p, maks_w = pravilni_podatki[0], pravilni_podatki[1], pravilni_podatki[2], pravilni_podatki[3]
        else: 
            pravilni_podatki = podatki(N, w, p) # uporabiva funkcijo podatki, ki podatke spremeni v pravo obliko
            N, w, p = pravilni_podatki[0], pravilni_podatki[1], pravilni_podatki[2] 
        if lamda == None or 0:
            maks_w = [c]* len(w)
            lamda = 0 
        if c < min(w):
            return [0, 0, 0, 0]
        if len(N) == len(w) == len(p) == len(maks_w): 
            pass
        else: 
            raise ValueError("Napačno vneseni podatki")
        #naredimo matrike z, k, n in nastavimo začetne pogoje
        z = matrika(lamda,c) #element matrike z[d][s] pomeni maksimalno vrednost pri
        for d in range(c + 1): #kapaciteti nahrbtnika d, pri čemer največ s predmetov spremeni
            for s in range(lamda + 1): #svojo težo na maks_w
                z[d][s]= float("-inf")
        z[0][0] = 0     
        c_zvezdica = 0

        k = matrika(lamda,c) #element matrike k[d][s] pomeni optimalno število predmetov v 
        for d in range(c + 1): #nahrbtniku pri kapaciteti nahrbtnika d, pri čemer največ s 
            for s in range(lamda + 1): #predmetov spremeni svojo težo na maks_w
                k[d][s]= 0
        k[0][0] = 0

        g = matrika(lamda,c) #element matrike g[d][s] pomeni optimalno število predmetov v 
        for d in range(c + 1): #v nahrbtniku iz množice N2 (druga polovica vseh stvari) pri
            for s in range(lamda + 1): #kapaciteti nahbrnika d, pri čemer največ s predmetov
                g[d][s] = 0 #spremeni svojo težo na maks_w
        g[0][0] = 0

        for j in range(len(N)): # izberemo j-ti predmet 
            for d in range(c, w[j]-1, -1):  # in ga poskusimo dodati v svoji nominalni teži 
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
