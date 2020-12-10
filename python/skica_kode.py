def solve_RKP(N, c, w, p, gama = None,  max_w = None):
    najprej uredimo podatke po padajoči teži (max_w - w)
    če je max_w = None, uredimo podatke padajoče po teži (w)
    naredimo matrike Z, K, G ter nastavimo začetne pogoje
    element v prvi vrstici in prvem stolpcu matrike nastavimo na 0 vse ostale na minus neskončno:
    for d in range(c + 1): 
        for s in range(gama + 1): 
            Z[d][s]= float("-inf")
    Z[0][0] = 0  
    analogno naredimo še matriki K in G
    izberemo j-ti predmet:
    for j in range(len(N)): 
        j-ti predmet poskusimo dodati v nahrbtnik v svoji nominalni teži pri pogoju, da smo že vstavili gama predmetov
        for d in range(c, w[j]-1, -1):  
            if Z[d - w[j]][gama] + p[j] > Z[d][gama]:
                Z[d][gama] = Z[d - w[j]][gama] + p[j] 
                K[d][gama] = 1 + K[d - w[j]][gama]
                if j  >= ((len(N) / 2)):
                    G[d][gama] = 1 + G[d - w[j]][gama]
        j-ti predmet poskusimo dodati v svoji robustni teži:            
        for s in range(gama, 0, -1):
            for d in range(c, maks_w[j] - 1, -1):
                if Z[d - maks_w[j]][s - 1] + p[j] > Z[d][s]:
                    Z[d][s] = Z[d - maks_w[j]][s - 1] + p[j]
                    K[d][s] = 1 + K[d - maks_w[j]][s-1] 
                    if j  >= ((len(N) / 2)):
                        G[d][s] = 1 + G[d - maks_w[j]][s - 1]
        največji člen matrike Z je z*:
        z* = max([max(i) for i in Z])
        pogledamo kje v matriki se nahaja z*:
        pozicija = [[index, vrstica.index(z_zvedica)] for index, vrstica in enumerate(Z) if z_zvedica in vrstica]
        vrstica ter stolpec maksimalne vrednosti predstavljata skupno težo vstavljenih predmetov:
        c* = pozicija[0][0]
        število_predmetov_s_povečano_težo = pozicija[0][-1] #to je število predmetov, ki se jim je spremenila teža

        najdemo k* ter g1, ki pomeni koliko elementov iz N2(druga polovica predmetov v N) je v optimalni rešitvi:
        g1 = G[c*][število_predmetov_s_povečano_težo] 
        k* = K[c*][število_predmetov_s_povečano_težo] 
        g* = k* - g1
        return [z*, c*, k*, g*]

def rekurzija(N, z*, k*, c*, gama, w, maks_w, p, vstavljeni_predmeti=[]):
    if len(N) == 1 and vstavljeni_predmeti == []:
        if gama != 0:
            if maks_w[0] <= c*:
                return N
        else:
            if w[0] <= c*:
                return N
    elif len(N) == 1 and vstavljeni_predmeti != []:
        if gama != 0:
            if maks_w[0] <= c*:
                vstavljeni_predmeti.append(N[0])
                return(vstavljeni_predmeti)
            else: 
                return(vstavljeni_predmeti)
        else:
            if w[0] <= c*:
                vstavljeni_predmeti.append(N[0])
                return(vstavljeni_predmeti)
    else:
        uredi predmete po padajoči vrednosti (maks_w - w)
        polovica =(len(N) / 2 )
        if n % 2 == 0: 
           N1, N2 = N[:polovica], N[polovica:]
           w1, w2 = w[:polovica], w[polovica:] 
           maks_w1, maks_w2 = maks_w[:polovica], maks_w[polovica:]
           p1, p2 = p[:polovica], p[polovica:]
        else:
           N1, N2 = N[:polovica + 1], w[polovica + 1:]
           w1, w2 = w[:polovica + 1], w[polovica + 1:] 
           maks_w1, maks_w2 = maks_w[:polovica + 1], maks_w[polovica + 1:]
           p1, p2 = p[:polovica + 1], p[1+ polovica:]
        if k* >= gama: 
            najdi tako kombinacijo c1 + c2 = c*, da bo 
            z1(c1) + z2(c2) = z*, pri čemer z1(c1) ter z1(c2)
            dobimo kot:
            z1(c1) = RKP(N1, c1, w1, p1, gama, maks_w1)[0] 
            z2(c2) = solve_KP(N2, c2, w2, p2)[1]
            solution_set_kp = solve_KP(N2, c2, w2, p2)[0]
            vstavljeni_predmeti.append(solution_set_kp)
            k1* = RKP(N1, c1, w1, p1, gama, maks_w1)[3]
            return rekurzija(N1, z1(c1) , k1*, c1, gama, w1, maks_w1, p1, vstavljeni_predmeti)        
        else: 
            najdi tako kombinacijo c1 + c2 = c*, da bo 
            z1(c1) + z2(c2) = z*, pri čemer z1(c1) ter z1(c2)
            dobimo kot:    
            z1(c1) = solve_eKkP(N1, c1, maks_w1, p1, k*)[1]
            z2(c2) = RKP(N2, c* - c1, w2, p2, gama - k*, maks_w2)[0]
            solution_set_eKkP = solve_eKkP(N1, c1, maks_w1, p1, k*)[0]
            k2* = RKP(N2, c2, w2, p2, gama - k*, maks_w2)[3]
            return rekurzija(N2, z2(c2), k2*, c2,gama - k*, w2, maks_w2, p2, vstavljeni_predmeti)