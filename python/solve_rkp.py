"""
Robustni Problem Nahrbtinka
"""

def matrika(m,n):
    return [[0] * (m+1) for _ in range(n+1)] #funkcija, ki naredi ničelno matriko m X n

def v_seznam(N):
    N0 = []
    for i in N:
        N0 += [i]
    N = N0
    return N

# funkcija, ki podatke razvrsti padajoče po maks_w(j)
def podatki(N, w, p, maks_w = None):
    N = v_seznam(N)
    if maks_w is None:
         vrstni_red = [i[0] for i in sorted(enumerate(w), key=lambda x:x[1])]
         w = [w[i] for i in vrstni_red]
         p = [p[i] for i in vrstni_red]
         N = [N[i] for i in vrstni_red]
         return (N[::-1], w[::-1], p[::-1])
    else:  
        urejen_sez = [0] * len(maks_w)
        for i in range(len(maks_w)):
            urejen_sez[i] = maks_w[i] - w[i]
        vrstni_red = [i[0] for i in sorted(enumerate(urejen_sez), key=lambda x:x[1])]
        maks_w = [maks_w[i] for i in vrstni_red]
        p = [p[i] for i in vrstni_red]
        w = [w[i] for i in vrstni_red]
        N = [N[i] for i in vrstni_red]
        return (N[::-1], w[::-1], p[::-1], maks_w[::-1])

# množico N razdeli na dva enako velika seznama N1 in N2
def particija(N):
    n = len(N)
    N = v_seznam(N)
    N1 = []
    N2 = []
    if n % 2 == 0:
        for el in N:
            if N.index(el) < (n / 2) :
                N1.append(el)
            else:
                N2.append(el)
        return N1, N2
    else:
        for el in N:
            if N.index(el) <= (n / 2):
                N1.append(el)
            else:
                N2.append(el)
        return N1, N2

# funkcija RKP vrne optimalno vrednost, optimalno težo pri tej vrednosti, koliko predmetov uporabimo in koliko predmetov uporabimo iz N1 (prve polovice predmetov)
def RKP(N, c, w, p, lamda = None,  maks_w = None):
    # slovar predmetov spremenimo v resitev predmetov
    N = v_seznam(N)
    # uporabiva funkcijo podatki, ki podatke spremeni v pravo obliko
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


# Solve_KP vrne seznam predmetov in optimalno vrednost, če je lamda = 0, torej to je navadni problem nahrbtnika
def solve_KP(N, c, w, p):  
    n = len(N)
    if n == 1:
        if w[0] <= c:
            return [N[0], p[0]]
        else:
            return [0, 0]
    
    else:
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
        z_zvezdica = z[n][c]
        z_zvezdica1 = z[n][c] 
        c_zvezdica = 0
        seznam_stvari = [] #seznam_stvari predstavlja seznam stvari, ki smo jih dali v nahrbtnik
        #set_stvari = []
        for i in range(n, 0, -1):  
            if z_zvezdica1 <= 0: #seznam stvari dobimo tako, da za vsak element i v obratnem vrstnem
                break            #redu pogledamo kakšna je optimalna vrednost, če v nahrbtnik lahko
            if z_zvezdica1 == z[i - 1][c]: #vstavimo samo elemente iz množice {0, 1, ..., i}
                continue                   #če je ta vrednost enaka optimalni vrednosti, potem nadaljujemo
            else:                           #če pa se ta vrednost razlikuje od optimalne vrednosti, potem element i
                N = v_seznam(N)            #dodamo v seznam stvari, zmanjšamo optimalno vrednost za vrednost 
                element = N[i - 1]         #tega elementa in nadaljujemo dokler optimalna vrednost ne pride do 0
                #set_stvari.append([element, w[i - 1], p[i - 1]])
                seznam_stvari.append(element)
                c_zvezdica += w[i - 1]
                z_zvezdica1 -= p[i - 1]
                c -= w[i - 1]
        return [seznam_stvari, z_zvezdica]

# solve_eKkP vrne seznam vseh predmetov in optimalno vrednost, če dodatno omejimo maksimalno števio uporabljenih predmetov 
def solve_eKkP(N, c, w, p, k):   #algoritem je tu podoben kot pri Solve_KP, le da je matrika k tridimenzionalna, saj zraven
    n = len(N)                 #beleži še kakšna je optimalna vrednost, če omejimo maksimalno število predmetov
    if n == 1:                  #na m = 1, ..., k
        if k == 0:
            return [0, 0]
        else: 
            if w[0] <= c:
                return [N[0], p[0]]
            else:
                return [0, 0]
    else:
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
                a = z[i - 1][c][k]
                continue
            else:
                element = N[i - 1]
                seznam_stvari.append(element)
                c_zvezdica += w[i - 1]
                z_zvezdica1 -= p[i - 1]
                c -= w[i - 1]
        return(seznam_stvari, z_zvezdica)

def naredi_pravi_seznam(resitev): #funkcija vgnezden seznam spremeni v navaden seznam
    nov_sez = []
    for el in resitev:
        if isinstance(el, list):
            for i in el:
                nov_sez.append(i)
        else:
            nov_sez.append(el)
    return(nov_sez)
#funkcija, ki deluje na principu rekurzije in nam vrne seznam stvari, ki jih vstavimo v nahrbtnik
def rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p, resitev=[]):
    if len(N) == 1 and resitev == []:
        if lamda != 0:
            if maks_w[0] <= c_zvezdica:
                print(N)
                return N
            else:
                print("V nahrbtnik ne moremo dati nobene stvari.")
        else:
            if w[0] <= c_zvezdica:
                return N
            else:
                print("V nahrbtnik ne moremo dati nobene stvari.")
    elif len(N) == 1 and resitev != []:
        if lamda != 0:
            if maks_w[0] <= c_zvezdica:
                resitev.append(N[0])
                resitev = naredi_pravi_seznam(resitev)
                return(resitev)
            else: 
                resitev = naredi_pravi_seznam(resitev)
                return(resitev)
        else:
            if w[0] <= c_zvezdica:
                resitev.append(N[0])
                resitev = naredi_pravi_seznam(resitev)
                return(resitev)
    else:
        N = v_seznam(N)
        N, w, p, maks_w = podatki(N, w, p, maks_w)
        N1, N2 = particija(N) #N razdelimo na N1 in N2
        n = len(N)  
        polovica = int((n / 2 ))
        if n % 2 == 0:     #tudi seznam, ki predstavlja vrednosti, teže in maks teže
           w1 = w[:polovica] #razdelimo na dva dela
           w2 = w[polovica:] 
           maks_w1 = maks_w[:polovica]
           maks_w2 = maks_w[polovica:]
           p1 = p[:polovica]
           p2 = p[polovica:]
        else:
           w1 = w[:polovica + 1]
           w2 = w[polovica + 1:] 
           maks_w1 = maks_w[:polovica + 1]
           maks_w2 = maks_w[polovica + 1:]
           p1 = p[:polovica + 1]
           p2 = p[1+ polovica:]
    
        if k_zvezdica >= lamda: #če je število vstavljenih predmetov iz prve polovice stvari večje
                                #od lamde (največ toliko predmetov lahko spremeni svojo težo iz w na maks w),
            for c_1 in range(c_zvezdica + 1): #potem seznam vstavljenih predmetov iz N2 dobimo s pomočjo
                c1 = c_1                      #funkcije Solve_KP, problem za predmete iz N1, kjer največ
                c2 = c1 - c_zvezdica          #lamda predmetov spremeni svojo težo, pa spet predstavlja 
                z1_c_1 = RKP(N1, c_1, w1, p1, lamda, maks_w1)[0] #robustni problem nahrbtnika, zato spet pokličemo
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w2, p2)[1] #funkcijo rekurzija
                z1_c1 = z1_c_1
                z2_c2 = z2_c_2
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
                    break
            solution_set_kp = solve_KP(N2, c2, w2, p2)[0]
            resitev.append(solution_set_kp)
            k1_zvezdica = RKP(N1, c1, w1, p1, lamda, maks_w1)[3]
            return rekurzija(N1, z1_c1 , k1_zvezdica, c1, lamda, w1, maks_w1, p1, resitev)        
        else: 
            for c_2 in range(c_zvezdica + 1):    #če je lamda večji od k, dobimo seznam predmetov iz množice
                c2 = c_2                      #N1 s pomočjo funkcije solve_ekkp, za N2 pa spet pokličemo funkcijo rekurzija
                c1 = c_zvezdica - c2
                z2_c_2 = RKP(N2, c_zvezdica - c1, w2, p2, lamda - k_zvezdica, maks_w2)[0]
                z1_c_1 = solve_eKkP(N1, c1, maks_w1, p1, k_zvezdica)[1]
                z1_c1 = z1_c_1
                z2_c2 = z2_c_2

                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c2 = c_2
                    c1 = c_zvezdica - c2
                    break
            solution_set_eKkP = solve_eKkP(N1, c1, maks_w1, p1, k_zvezdica)[0]
            resitev.append(solution_set_eKkP)
            k2_zvezdica = RKP(N2, c2, w2, p2, lamda - k_zvezdica, maks_w2)[3]
            c2 = c_zvezdica - c1
            return rekurzija(N2, z2_c2, k2_zvezdica, c2,lamda - k_zvezdica, w2, maks_w2, p2, resitev)
 
def resitev(N, c, w, p, lamda = None, maks_w = None): #funkcija nam vrne končno rešitev: 
    k_zvezdica = RKP(N, c, w, p, lamda, maks_w)[3]     #seznam vstavljenih predmetov in vrednost
    z_zvezdica = RKP(N, c, w, p, lamda, maks_w)[0]
    c_zvezdica = RKP(N, c, w, p, lamda, maks_w)[1]
    resitev = rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p)
    while resitev != naredi_pravi_seznam(resitev):
        resitev = naredi_pravi_seznam(resitev)
    mnozica = set()
    if resitev != []:
        for i in resitev:       #če je slučajno v seznamu predmetov tudi element 0,
            mnozica.add(i)       #ga odstranimo, saj se v funkciji rekurzija zaradi lažjega
        resitev = v_seznam(mnozica)  #poteka v primeru, da ne vstavimo nobenega elementa v seznam
        if resitev[0] == 0:          #vstavi 0
            resitev = resitev[1:]
    return(resitev, z_zvezdica)

def preberi_podatke(dat, kodna_tabela='utf-8'): #prebere podatke iz mape INSTANCES
    with open(dat, encoding=kodna_tabela) as datoteka: #dobimo seznam elementov in                              
        N = []                                #njihovih vrednosti, teže in maks teže
        w = []
        p = []
        maks_w = []
        for vrstica in datoteka:
            x = []
            x = vrstica.split()
            N.append(int(x[0]))
            p.append(int(x[1]))
            w.append(int(x[2]))
            maks_w.append(int(x[3]))
    
    return(N, w, p, maks_w)


# ta funkcija prebere podatke iz S&P 500.txt in jih prilagodi, tako da potem dela program preberi_podatke_za_delnice() 
def popravi_podatke(dat, kodna_tabela="utf-8"):
    with open(dat, encoding=kodna_tabela) as datoteka:
        N = []
        w = []
        r = []
        ime_podjetja = []
        kratica_podjetja = []
        maks_w = []
        števec = 0
        for vrstica in datoteka:
            vrstica = vrstica.rstrip()
            števec += 1
            if števec > 1:
                x = []
                x = vrstica.split(",")
                if len(x) == 7:
                    N.append(x[0])
                    kratica_podjetja.append(x[1])
                    ime_podjetja.append(x[2])
                    w.append(float(x[4]))
                    maks_w.append(float(x[5]))
                    r.append(x[6])
                else:                  
                    N.append((x[0]))
                    kratica_podjetja.append(x[1])
                    ime_podjetja.append(x[2])
                    w.append(float(x[3]))
                    maks_w.append(float((x[4])))
                    r.append((x[5]))
                #print(ime_podjetja)
    with open("Robust-knapsack-problem/podatki/podatki za delnice/popravljeni_podatki.txt","w") as nova_datoteka:
        for i in range(len(N)):
            nova_datoteka.write("{} {} {} {} {} {}\n".format(int(N[i].strip('""')), kratica_podjetja[i], ime_podjetja[i], w[i], maks_w[i], float(r[i].strip('""'))))


#popravi_podatke("Robust-knapsack-problem/podatki/podatki za delnice/S&P 500.txt")

import random
def naredi_podatke(stevilo, teza, max_cena): #funkcija zgenerira naključne podatke
    n = random.randint(1, stevilo)
    c = random.randint(0, teza)
    lamda = random.randint(0, n)
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

    return [N, c, w, p, lamda, maks_w]

def preberi_podatke_za_delnice(dat, budget, kodna_tabela='utf-8'): #funkcija prebere podatke o delnicah
    with open(dat, encoding=kodna_tabela) as datoteka:
        N = []
        maks_p = []
        p = []
        r = []
        imena_delnic = []
        vse_delnice = 0
        seznam_kolicine_delnic = []
        for vrstica in datoteka:
            x = []
            x = vrstica.split() #najprej vsako vrstico razdelimo na seznam
            a = x[-1]            
            imena_delnic.append(x[1]) #prvi element vsake vrstice predstavlja ime delnice
            stevilo_delnic = int(budget / float(x[-2])) #maksimalno število delnic posameznega podjetja, ki jih lahko kupimo (budget / maks cena delnice)
            seznam_kolicine_delnic.append(stevilo_delnic) #seznam, ki predstavlja največ koliko delnic posameznega podjetja lahko kupimo
            for delnica in range(vse_delnice + 1, vse_delnice + stevilo_delnic + 1): #naredimo nov seznam delnic, cen, maks cen in donosov
                N.append(delnica)                                                   #tu se vsaka posamezna delnica vsakega podjetja steje kot en element
                if float(x[-1]) > 0:
                    p.append(int(float(x[-3])))
                    maks_p.append(int(float(x[-2])))
                    r.append(int(float(x[-3]) * (1 + 0.01 * (float(x[-1])))))
                    vse_delnice += 1
                else:
                    p.append(0)   #če je donos negativen, nastavimo ceno, maks ceno in donos na 0,
                    maks_p.append(0)  #saj je ob pogoju, da želimo maksimirati dobiček, nesmiselno,
                    r.append(0)         #da v portfelj vstavimo tako delnico
                    vse_delnice += 1
    return(N, p, maks_p, r, seznam_kolicine_delnic, imena_delnic)


# preberi_podatke_za_delnice("Robust-knapsack-problem/podatki/podatki za delnice/prvih_11.txt",100)
    
from collections import Counter

def resitev_za_delnice(N, c, w, p, lamda, maks_w, seznam_kolicine_delnic, imena_delnic):
    resitev1 = resitev(N,c,w,p,lamda,maks_w)[0]
    nov_seznam = []
    seznam_delnic = []
    for i in range(1, len(seznam_kolicine_delnic) + 1):  #iz seznama, ki ga dobimo pri rekurziji je potrebno 
        a = seznam_kolicine_delnic[i - 1]              #še razbrati za delnice katerih podjetij gre in koliko 
        nov_seznam += ([i] * a)                        #delnic imamo za vsako podjetje
    for delnica in resitev1:
        seznam_delnic.append(nov_seznam[int(delnica) - 1])
    stevec = Counter()
    seznam_imen = []
    for delnica in seznam_delnic:
        seznam_imen.append(imena_delnic[delnica - 1])
    for delnica in seznam_imen:
        stevec[delnica] += 1 

    return(stevec, z_zvezdica)

#print(preberi_podatke('N_symbol_Company_price_maxprice_er.txt', 300))
#N, p, maks_p, r, seznam_kolicine_delnic, imena_delnic = (preberi_podatke_za_delnice('podatki\podatki za delnice\prvih_11.txt', 100))
#print(resitev_za_delnice(N, 100, p, r, 2, maks_p, seznam_kolicine_delnic, imena_delnic))



##### ČE ŠE NIMAŠ SI MOREŠ ZAGNAT TOLE V TERMINALU ###
# python3 -m pip install pillow v bash (terminal)

# pip install pillow (za windows)

import tkinter as tk

from PIL import Image, ImageTk



class PRVO_OKNO:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.geometry("450x225+500+300")
        self.button1 = tk.Button(self.frame, text = "Navadni problem nahrbtnika", width = 25, height = 5, command = self.new_window_problem_nahrbtnika)
        self.button2 = tk.Button(self.frame, text = "Robustni problem nahrbtnika", width = 25, height = 5, command = self.new_window_ROBUSTNI_PROBLEM_nahrbtnika)
        self.label1 = tk.Label(self.frame,text = "Kakšen tip problema imate?", height = 2)
        self.label1.grid()
        self.button1.grid()
        self.button2.grid()
        self.frame.pack()

    def new_window_problem_nahrbtnika(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app2 = NAVADNI_PROBLEM(self.newWindow)
        
        

    def new_window_ROBUSTNI_PROBLEM_nahrbtnika(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ROBUSTNI_PROBLEM(self.newWindow)
        
    

class NAVADNI_PROBLEM:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Navadni problem nahrbtnika")
        self.master.geometry("570x400+450+250")
        #gumbi 
        self.shrani_in_naprej1 = tk.Button(self.frame, text = 'Naprej', width = 12, command = self.shrani_in_naprej3)
        self.naslov = tk.Label(self.frame, text= "Kratek opis problema")
        self.quitButton = tk.Button(self.frame, text = 'Zapri', width = 5, command = self.close_windows)
        self.backButton = tk.Button(self.frame, text = 'Nazaj', width = 5, command = self.nazaj)
        self.stevilo_podatkov = tk.Entry(self.frame, width=20, selectborderwidth=2,bg= "gray90")
        self.prazno_polje1 = tk.Label(self.frame,text = "", width = 3,height=5)
        self.label1 = tk.Label(self.frame, anchor="e", text = "Preprosti problem nahrbtnika je računalniški problem, s katerim poskusimo \nzapolniti nahrbtnik z danimi predmeti, ki ima vsak svojo ceno in težo. Bodisi\n gre za dejansko polnjenje nahrbtnika, polnjenje nakupovalne vreče, zlaganje\npredmetov v avto. Deluje po principu, da bi karseda najbolje zapolnili prostor in vzeli\n s sabo predmete s čimvišjo vrednostjo. Na naslednji strani boste v program \nzapisali naslednje podatke, 1. maksimalno kapaciteto nahrbtnika, 2. nominalno\n težo predmetov in 3. vrednosti predmetov")
        #self.label1 = tk.Label(self.frame,text = "Robustni problem nahrbtnika je nekakšna nadgranja problema nahrbtnika. Dodaten \nproblem se pojavi pri točnosti naših podatkov, in sicer pri utežeh. Za vsako težo\n predmeta vemo njegovo zgornjo in spodnjo mejo, ampak spodnja meja nas ne skrbi,\nsaj če bo predmet lažji to ne bo vplivalo na optimalno skupno vrednost. Na naslednji \nstrani boste v program zapisali naslednje podatke: 1. maksimalno kapaciteto \nnahrbtnika, 2. nominalno težo predmetov, 3. robustno težo predmetov, \n4. maksimalno število koliko predmetov spremeni svojo težo.")
        #self.fake = tk.Label(self.master,text = "", width = 20, height= 5)
        self.druga = tk.Label(self.frame, text= "",width = 13)
        self.tretja = tk.Label(self.frame, text= "",width = 30)
        self.cetrta = tk.Label(self.frame,height = 16)
        self.peta = tk.Label(self.frame ,height = 10)

        # slika
        image = Image.open("Robust-knapsack-problem/python/nahrbtnik.jpg")
        image = image.resize((250, 220), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.slika1 = tk.Label(self.frame, image=photo)
        self.slika1.image = photo


        # prikaz
        #self.slika.grid(row=2,column=1)
        
        self.backButton.grid(row=0, column=0)
        self.quitButton.grid(row=0, column=1)
        self.naslov.grid(row=0, column=3)
        self.druga.grid(row=0, column = 2)
        self.tretja.grid(row=0, column = 4)
        self.cetrta.grid(row=1, column = 0)
        self.peta.grid(row=2, column = 0)
        #self.fake.grid(row=1, column=3)

        self.label1.place(x=25, y= 25)

        self.slika1.place(x=163,y=169)
        self.prazno_polje1.grid(row=1, column = 2)
        self.shrani_in_naprej1.grid(row=1,column= 3)
        
        self.frame.grid()
        # label(self.frame,text = "", height= 6)
        

        
    def shrani_in_naprej3(self):
        #self.master.destroy()
        self.newWindow = tk.Toplevel(self.master)
        self.app3 = NAVADNI_PROBLEM_NADALJEVANJE(self.newWindow)
          
    
    def close_windows(self):
        self.master.destroy()

    def nazaj(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PRVO_OKNO(self.newWindow)


class ROBUSTNI_PROBLEM:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Robustni problem nahrbtnika")
        self.master.geometry("570x400+450+250")
        #gumbi 
        self.shrani_in_naprej1 = tk.Button(self.frame, text = 'Naprej', width = 12, command = self.shrani_in_naprej2)
        self.naslov = tk.Label(self.frame, text= "Kratek opis problema")
        self.quitButton = tk.Button(self.frame, text = 'Zapri', width = 5, command = self.close_windows)
        self.backButton = tk.Button(self.frame, text = 'Nazaj', width = 5, command = self.nazaj)
        self.stevilo_podatkov = tk.Entry(self.frame, width=20, selectborderwidth=2,bg= "gray90")
        self.prazno_polje1 = tk.Label(self.frame,text = "", width = 3,height=5)
        self.label1 = tk.Label(self.frame,text = "Robustni problem nahrbtnika je nekakšna nadgranja problema nahrbtnika. Dodaten \nproblem se pojavi pri točnosti naših podatkov, in sicer pri utežeh. Za vsako težo\n predmeta vemo njegovo zgornjo in spodnjo mejo, ampak spodnja meja nas ne skrbi,\nsaj če bo predmet lažji to ne bo vplivalo na optimalno skupno vrednost. Na naslednji \nstrani boste v program zapisali naslednje podatke: 1. maksimalno kapaciteto \nnahrbtnika, 2. nominalno težo predmetov, 3. robustno težo predmetov, 4. vrednosti\npredmetov in 5. maksimalno število koliko predmetov spremeni svojo težo.")
        self.fake = tk.Label(self.master,text = "Jan", width = 20, height= 5)
        self.druga = tk.Label(self.frame, text= "",width = 10)
        self.tretja = tk.Label(self.frame, text= "",width = 30)
        self.cetrta = tk.Label(self.frame,height = 16)
        self.peta = tk.Label(self.frame ,height = 10)
        # slika
        image = Image.open("Robust-knapsack-problem/python/knapsack.png")
        image = image.resize((219, 219), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.slika1 = tk.Label(self.frame, image=photo)
        self.slika1.image = photo


        # prikaz
        #self.slika.grid(row=2,column=1)
        
        self.backButton.grid(row=0, column=0)
        self.quitButton.grid(row=0, column=1)
        self.naslov.grid(row=0, column=3)
        self.druga.grid(row=0, column = 2)
        self.tretja.grid(row=0, column = 4)
        self.cetrta.grid(row=1, column = 0)
        self.peta.grid(row=2, column = 0)
        #self.fake.grid(row=1, column=3)

        self.label1.place(x=25, y= 25)
        self.slika1.place(x=163,y=169)
        self.prazno_polje1.grid(row=1, column = 2)
        self.shrani_in_naprej1.grid(row=1,column= 3)
        
        self.frame.grid()

    def shrani_in_naprej2(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app4 = ROBUSTNI_PROBLEM_NADALJEVANJE(self.newWindow)

    def nazaj(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PRVO_OKNO(self.newWindow)

    def close_windows(self):
        self.master.destroy()

class NAVADNI_PROBLEM_NADALJEVANJE:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Robustni problem nahrbtnika")
        self.master.geometry("590x284+440+300")
        
        # gumbi 
        self.gumb_resitev = tk.Button(self.frame, text = "Prikaži rešitev", width = 25, command = self.resitev_problema)
        self.vprasanje_kapaciteta = tk.Label(self.master, text="1. Zapišite kapaciteto nahrbtnika, npr. 10")
        self.vprasanje_teza = tk.Label(self.master, text="2. Zapišite teže predmetov v pravilnem vrstnem redu, npr. 1,3,5,2,5 za 5 predmetov")
        self.vprasanje_vrednost = tk.Label(self.master, text="3. Zapišite vrednosti predmetov v pravilnem vrstnem redu, npr. 10,30,50,20,52 za 5 predmetov")
        self.kapaciteta = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.teza = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.vrednost = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.lbl_value = tk.Label(self.master, text="0")
        self.quitButton2 = tk.Button(self.frame, text = 'Zapri', width = 25, command = self.close_all)
        
        # grid
        self.vprasanje_kapaciteta.grid(row=0, column=0)
        self.kapaciteta.grid(row=1,column=0)
        self.vprasanje_teza.grid(row=2, column=0)
        self.teza.grid(row=3, column=0)
        self.vprasanje_vrednost.grid(row=4, column=0)
        self.vrednost.grid(row=5, column=0)
        self.gumb_resitev.grid(row=5,column=0)
        self.lbl_value.grid(row=6, column=0)
        self.frame.grid()
        self.quitButton2.grid(row= 8, column=0)
   
    def resitev_problema(self):
        kapaciteta_c = self.kapaciteta.get()
        try:
            int(kapaciteta_c)
        except ValueError:
            kapaciteta_c = 0
            self.lbl_value["text"] = f"Napaka v vnosu kapacitete"
        
        kapaciteta_c = int(self.kapaciteta.get())
        if kapaciteta_c < 0:
            kapaciteta_c = 0

        w = [(self.teza.get())]
        p = [self.vrednost.get()]
        w1 = []
        for i in w[0].split(","):
            if i != ",":
                w1 += [int(i)]
        p1 = []
        for i in p[0].split(","):
            if i != ",":
                p1 += [int(i)]
        p = p1     
        w = w1
        N = set()
        for i in range(1,len(p) + 1):
            N.add(i)
        print(w,N)
        seznam = solve_KP(N, kapaciteta_c, w, p)
        pravi_seznam = seznam[0]
        z_zvezdica = seznam[1]
        pravi_seznam = sorted(pravi_seznam)
        pravi_seznam2 = set()
        for i in pravi_seznam:
            pravi_seznam2.add(i)
        koncni_seznam = v_seznam(pravi_seznam2)
        self.lbl_value["text"] = f"seznam predmetov, ki jih dodamo v nahrbtnik {koncni_seznam} \n in optimalna vrednost predmetov je {z_zvezdica}"

    def close_all(self):
        self.master.destroy()

class ROBUSTNI_PROBLEM_NADALJEVANJE:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Robustni problem nahrbtnika")
        self.master.geometry("600x370+440+270")
        
        # gumbi 
        self.gumb_resitev = tk.Button(self.frame, text = "Prikaži rešitev", width = 25, command = self.resitev_problema)
        self.vprasanje_kapaciteta = tk.Label(self.master, text="1. Zapišite kapaciteto nahrbtnika, npr. 10")
        self.vprasanje_teza = tk.Label(self.master, text="2. Zapišite teže predmetov v pravilnem vrstnem redu, npr. 1,3,3,2,5 za 5 predmetov")
        self.vprasanje_vrednost = tk.Label(self.master, text="4. Zapišite vrednosti predmetov v pravilnem vrstnem redu, npr. 10,30,50,20,52 za 5 predmetov")
        self.vprasanje_maks_w = tk.Label(self.master, text="3. Zapišite maksimalne teže predmetov v pravilnem vrstnem redu, npr. 2,4,3,3,5 za 5 predmetov")
        self.vprasanje_lamda = tk.Label(self.master, text="5. Zapišite največ koliko predmetov lahko spremeni svojo težo \n (število med 1 in številom predmetov) npr. 3")
        self.lamda = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.kapaciteta = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.teza = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.teza_maks_w = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.vrednost = tk.Entry(self.master, width = 20, selectborderwidth=2, bg= "gray90")
        self.lbl_value = tk.Label(self.master, text="0")
        self.quitButton2 = tk.Button(self.frame, text = 'Zapri', width = 25, command = self.close_all)

        # grid
        self.vprasanje_kapaciteta.grid(row=0, column=0)
        self.kapaciteta.grid(row=1,column=0)
        self.vprasanje_teza.grid(row=2, column=0)
        self.teza.grid(row=3, column=0)
        self.vprasanje_maks_w.grid(row=4, column=0)
        self.teza_maks_w.grid(row=5,column=0)
        self.vprasanje_vrednost.grid(row=6, column=0)
        self.vrednost.grid(row=7, column=0)
        self.vprasanje_lamda.grid(row=8, column=0)
        self.lamda.grid(row=9, column=0)
        self.gumb_resitev.grid(row=10, column=0)
        self.lbl_value.grid(row=11, column=0)
        self.quitButton2.grid(row= 12, column=0)
        self.frame.grid()


        self.števec = 0
    def resitev_problema(self):
        kapaciteta_c = self.kapaciteta.get()
        try:
            int(kapaciteta_c)
        except ValueError:
            kapaciteta_c = 0
            self.lbl_value["text"] = f"Napaka v vnosu kapacitete"
        
        kapaciteta_c = int(self.kapaciteta.get())
        if kapaciteta_c < 0:
            kapaciteta_c = 0
        
        w = [(self.teza.get())]
        p = [self.vrednost.get()]
        maks_w = [self.teza_maks_w.get()]
        lamda = int(self.lamda.get())
        w1 = []
        for i in w[0].split(","):
            if i != ",":
                w1 += [int(i)]
        p1 = []
        for i in p[0].split(","):
            if i != ",":
                p1 += [int(i)]
        maks_w1 = []
        for i in maks_w[0].split(","):
            if i != ",":
                maks_w1 += [int(i)]
        p = p1
        maks_w = maks_w1     
        w = w1
        N = set()
        for i in range(1,len(p) + 1):
            N.add(i)

        seznam = resitev(N,kapaciteta_c, w, p, lamda, maks_w)
        pravi_seznam = seznam[0]
        z_zvezdica = seznam[1]
        self.lbl_value["text"] = f"seznam predmetov, ki jih dodamo v nahrbtnik {pravi_seznam} \n in optimalna vrednost predmetov je {z_zvezdica}"

        
    def close_all(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ROBUSTNI_PROBLEM_NADALJEVANJE(self.newWindow)
        self.master.destroy()



def main(): 
    okno = tk.Tk()
    app1 = PRVO_OKNO(okno)
    okno.geometry("450x225+500+300")
    okno.title("Problem nahrbtnika")
    okno.mainloop()

if __name__ == '__main__':
     main()



#Vprašanja: 
