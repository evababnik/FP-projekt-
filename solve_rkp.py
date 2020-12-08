"""
Robustni Problem Nahrbtinka
"""



def matrika(m,n):
    return [[0] * (m+1) for _ in range(n+1)]

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

# primer
#print(podatki([1,2,3,4,5,6,7],[20,19,18,17,16,15,14],[20,10,14,13,11,2,24],[10,10,10,10,10,10,10]))


# množico razdeli na dva enako velika seznama
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
    # slovar predmetov spremenimo v seznam predmetov
    N = v_seznam(N)
    # uporabiva funkcijo podatki, ki podatke spremeni v pravo obliko
    if len(N) == 1:
        if lamda != 0:
            if maks_w[0] <= c:
                return [p[0], maks_w[0], 1, 0]   
            else:
                return [0, 0, 0, 0]
        else:
            if w[0] <= c:
                return [p[0], w[0], 1, 0]
            else:
                return [0, 0, 0, 0]
    else:
        if maks_w is not None:
            pravilni_podatki = podatki(N, w, p, maks_w)
            N, w, p, maks_w = pravilni_podatki[0], pravilni_podatki[1], pravilni_podatki[2], pravilni_podatki[3]
        else: 
            pravilni_podatki = podatki(N, w, p)
            N, w, p = pravilni_podatki[0], pravilni_podatki[1], pravilni_podatki[2]
    
        if lamda is not None:
            if lamda > len(N):
                lamda = len(N)
                print("Lamda je večja kot moč množice predmetov, zato sva lamdo nastavila na", len(N))
        if lamda == None or 0:
            maks_w = [c]* len(w)
            lamda = 0
        if c < min(w):
            return [0, 0, 0, 0]
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
        return [z_zvedica, c_zvezdica, k_zvezdica, g_zvezdica]

# primer:
# print(RKP({1,2,3}, 7, [2,2,3], [4, 5, 6], 2, [4, 4, 3]))
# print(RKP({1,2,3,4,5,6,7,8,9,10,11,12}, 20, [2,2,3,40,5,2, 2,3,4,5, 1,14], [4, 5, 6, 4, 2, 4, 5, 6, 4, 2, 2,15]))
# RKP([1,2,3,4,5,6], 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])
# RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])
# RKP({1,2,3,4,5,6}, 6, [1,1,1,2,3,9],[2,3,4,5,5,3])

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
        seznam_stvari = []
        set_stvari = []
        for i in range(n, 0, -1):
            if z_zvezdica1 <= 0:
                break
            if z_zvezdica1 == z[i - 1][c]:
                continue
            else:
                N = v_seznam(N)
                element = N[i - 1]
                set_stvari.append([element, w[i - 1], p[i - 1]])
                seznam_stvari.append(element)
                c_zvezdica += w[i - 1]
                z_zvezdica1 -= p[i - 1]
                c -= w[i - 1]
        return [seznam_stvari, z_zvezdica]

#solve_KP([1,2,3], 2, [1,1,1], [3,4,3])
#solve_KP({1,2,3,4,5,6}, 6, [1,1,1,2,3,9],[2,3,4,5,5,3])

# solve_eKkP vrne seznam vseh predmetov in optimalno vrednost, če dodatno omejimo maksimalno števio uporabljenih predmetov s k 
# rezulatat v smislu ([[4, 4, 3], [3, 6, 5]], 8), kar pomeni 4 predmet, teža = 4, vrednost 3 in 3 predmet, teža 6 in 5 vrednost.
def solve_eKkP(N, c, w, p, k):
    N = v_seznam(N)
    n = len(N)
    if n == 1:
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
        set_stvari = []
        seznam_stvari = []
        for i in range(n, 0, -1):
            if z_zvezdica1 <= 0:
                break
            elif z_zvezdica1 == z[i - 1][c][k]:
                continue
            else:
                element = N[i - 1]
                #set_stvari.append([element, w[i - 1], p[i - 1]])
                seznam_stvari.append(element)
                c_zvezdica += w[i - 1]
                z_zvezdica1 -= p[i - 1]
                c -= w[i - 1]
        return(seznam_stvari, z_zvezdica)

def naredi_pravi_seznam(seznam):
    nov_sez = []
    for el in seznam:
        if isinstance(el, list):
            for i in el:
                nov_sez.append(i)
        else:
            nov_sez.append(el)
    return(nov_sez)

def rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p, seznam=[]):
    if len(N) == 1 and seznam == []:
        if lamda != 0:
            if maks_w[0] <= c_zvezdica:
                print(N)
                return N
            else:
                #glede na to da je to rekurzija mislim da do tegale sploh ne more prit, pač da prej že vse te stavri preveri
                # sam škodit ne more :D 
                print("V nahrbtnik ne moremo dati nobene stvari.")
        else:
            if w[0] <= c_zvezdica:
                return N
            else:
                print("V nahrbtnik ne moremo dati nobene stvari.")
    elif len(N) == 1 and seznam != []:
        if lamda != 0:
            if maks_w[0] <= c_zvezdica:
                seznam.append(N[0])
                resitev = naredi_pravi_seznam(seznam)
                return(resitev)
            else: 
                resitev = naredi_pravi_seznam(seznam)
                return(seznam)
        else:
            if w[0] <= c_zvezdica:
                seznam.append(N[0])
                resitev = naredi_pravi_seznam(seznam)
                return(seznam)
    else:
        N = v_seznam(N)
        N, w, p, maks_w = podatki(N, w, p, maks_w)
        N1, N2 = particija(N) #N razdelimo na N1 in N2
        n = len(N)  
        polovica = int((n / 2 ))
        if n % 2 == 0:
           w1 = w[:polovica]
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
    
        if k_zvezdica >= lamda:
           
            for c_1 in range(c_zvezdica + 1):
                z1_c_1 = RKP(N1, c_1, w1, p1, lamda, maks_w1)[0]
                z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w2, p2)[1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
                    break
            solution_set_kp = solve_KP(N2, c2, w2, p2)[0]
            seznam.append(solution_set_kp)
            k1_zvezdica = RKP(N1, c1, w1, p1, lamda, maks_w1)[3]
            return rekurzija(N1, z1_c1 , k1_zvezdica, c1, lamda, w1, maks_w1, p1, seznam)        
        else: 
            for c_1 in range(c_zvezdica + 1):
                
                z2_c_2 = RKP(N2, c_zvezdica - c_1, w2, p2, lamda - k_zvezdica, maks_w2)[0]
                z1_c_1 = solve_eKkP(N1, c_1, w1, p1, k_zvezdica)[1]
                if z1_c_1 + z2_c_2 == z_zvezdica:
                    z2_c2 = z2_c_2
                    z1_c1 = z1_c_1
                    c1 = c_1
                    c2 = c_zvezdica - c1
                    break
            solution_set_eKkP = solve_eKkP(N1, c1, w1, p1, k_zvezdica)[0]
            seznam.append(solution_set_eKkP)
            k2_zvezdica = RKP(N2, c2, w2, p2, lamda - k_zvezdica, maks_w2)[3]
            c2 = c_zvezdica - c1
            return rekurzija(N2, z2_c2, k2_zvezdica, c2,lamda - k_zvezdica, w2, maks_w2, p2, seznam)
 
def resitev(N, c, w, p, lamda = None, maks_w = None):
    k_zvezdica = RKP(N, c, w, p, lamda, maks_w)[3]
    z_zvezdica = RKP(N, c, w, p, lamda, maks_w)[0]
    c_zvezdica = RKP(N, c, w, p, lamda, maks_w)[1]
    seznam = rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p)
    return(seznam, z_zvezdica)



# TALE DELA
#resitev([1,2,3,4, 5],9,[1,2, 3, 1, 2], [4,5,5,3, 2], 1,[3,3,3,3, 2])

#1 primer:
# kkk = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[3]
# zzz = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[0]
# ccc = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[1]
# lamda = 1
# N = [1,2,3,4, 5]
# w = [1,2, 3, 1, 2]
# maks_w = [3,3,3,3, 2]
# p = [4,5,5,3, 2]
# print(ccc)
# print(zzz)
# print(kkk)
# print(podatki([1, 2, 3, 4, 5], [1, 2, 3, 1, 2], [4, 5, 5, 3, 2], [3, 3, 3, 3, 2]))
# rekurzija(N, zzz, kkk, ccc, lamda, w, maks_w, p)

# 2. primer

# kkk, zzz, ccc = RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[3], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[0], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[1]
# lamda = 0
# N = {1,2,3,4,5,6}
# w = [1,1,1,2,3,1]
# maks_w = [3,3,3,3,3,3]
# p = [2,3,4,5,5,3]
# rekurzija(N, zzz, kkk, ccc, lamda, w, maks_w, p)

#3. primer 

# kkk, zzz, ccc = RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[3], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[0], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[1]
# lamda = 0
# N = {1,2,3,4,5,6}
# w = [1,1,1,2,3,1]
# maks_w = [3,3,3,3,3,3]
# p = [2,3,4,5,5,3]
# rekurzija(N, zzz, kkk, ccc, lamda, w, maks_w, p)


import random
def naredi_podatke(stevilo, teza, max_cena):
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
        self.master.geometry("470x284+500+300")
        #gumbi 
        self.komentar = tk.Label(self.frame, text= " napišite celo število, npr. 5 \n \n \n \n \n \n \n \n \n \n \n \n")
        self.shrani_in_naprej = tk.Button(self.frame, text = 'Naprej', width = 12, command = self.shrani_in_naprej1)
        self.quitButton = tk.Button(self.frame, text = 'Zapri', width = 5, command = self.close_windows)
        self.backButton = tk.Button(self.frame, text = 'Nazaj', width = 5, command = self.nazaj)
        self.stevilo_podatkov = tk.Entry(self.frame, width=20, selectborderwidth=2,bg= "gray90")
        self.prazno_polje = tk.Label(self.frame, text = '', width = 15)
        self.label1 = tk.Label(self.frame,text = "Koliko predmetov imate? ")
        self.prazno_polje1 = tk.Label(self.frame,text = "", width = 3)
        #self.prazno_polje2 = tk.Label(self.frame,text = "", height= 6)
        # slika
        image = Image.open("Robust-knapsack-problem/nahrbtnik.jpg")
        image = image.resize((250, 220), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.slika = tk.Label(self.frame, image=photo)
        self.slika.image = photo


        # prikaz
        #self.slika.grid(row=2,column=1)
        self.slika.place(x=205, y=50)
        #self.prazno_polje2.grid(row=3, column =0)
        self.shrani_in_naprej.place(x=40, y=80)
        self.komentar.grid(row=2, column=0)
        self.stevilo_podatkov.grid(row=1, column=0) 
        self.prazno_polje1.grid(row=2, column=2)
        self.prazno_polje.grid(row=1, column=1)
        self.label1.grid(row=0, column=0)
        self.backButton.grid(row=0, column=4)
        self.quitButton.grid(row=0, column=5)
        self.frame.grid()
        
    def shrani_in_naprej1(self):
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
        self.label1 = tk.Label(self.frame,text = "Robustni problem nahrbtnika je nekakšna nadgranja problema nahrbtnika. Dodaten \nproblem se pojavi pri točnosti naših podatkov, in sicer pri utežeh. Za vsako težo\n predmeta vemo njegovo zgornjo in spodnjo mejo, ampak spodnja meja nas ne skrbi,\nsaj če bo predmet lažji to ne bo vplivalo na optimalno skupno vrednost. Na naslednji \nstrani boste v program zapisali naslednje podatke: 1. maksimalno kapaciteto \nnahrbtnika, 2. nominalno težo predmetov, 3. robustno težo predmetov, \n4. maksimalno število koliko predmetov spremeni svojo težo.")
        self.fake = tk.Label(self.master,text = "Jan", width = 20, height= 5)
        self.druga = tk.Label(self.frame, text= "",width = 10)
        self.tretja = tk.Label(self.frame, text= "",width = 30)
        self.cetrta = tk.Label(self.frame,height = 16)
        self.peta = tk.Label(self.frame ,height = 10)
        # slika
        image = Image.open("Robust-knapsack-problem/knapsack.png")
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
        #self.mnozica_N = self.stevilo_podatkov.get()
        #print(self.mnozica_N)
        #self.master.destroy()
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
        kapaciteta_c = int(self.kapaciteta.get())
        # if type(kapaciteta_c) == type(1):
        #     kapaciteta_c = 0
        # else: 
        #     pass
        #     if kapaciteta_c < 0:
        #         kapaciteta_c = 0

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

        #primer
        # solve_KP([1,2,3], 2, [1,1,1], [3,4,3])
        # rešitev [1,2], 7
        #solve_KP({1,2,3,4,5,6,7}, 6, [1,1,1,2,3,9,1],[2,3,4,5,5,3,10])
        #rešitev [[4, 3, 2, 1], 14]
        #solve_KP({1,2,3,4,5}, 10, [1,3,3,2,4],[10,30,20,20,22])
        # [[5, 4, 2, 1], 82]

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

        
        self.števec += 1
        print(self.števec)
        #print(N)
        #N, w, p, maks_w = podatki(N,w,p,maks_w)
        #print(N)


        ###### ZAKAJ SI TA SEZNAM MAGIČNO VEDNO ZAPOMNE PREJŠNO REŠITEV??? 
        if self.števec == 1:
            self.seznam = resitev(N,kapaciteta_c, w, p, lamda, maks_w)
            print(self.seznam)
            self.pravi_seznam = self.seznam[0]
            self.z_zvezdica = self.seznam[1]
        #pravi_seznam = sorted(pravi_seznam)
            self.pravi_seznam2 = set()
            if self.pravi_seznam != []:
                for i in self.pravi_seznam:
                    self.pravi_seznam2.add(i)
                self.koncni_seznam = v_seznam(self.pravi_seznam2)
                if self.koncni_seznam[0] == 0:
                    self.koncni_seznam = self.koncni_seznam[1:]
            else:
                self.koncni_seznam = []
        self.lbl_value["text"] = f"seznam predmetov, ki jih dodamo v nahrbtnik {self.koncni_seznam} \n in optimalna vrednost predmetov je {self.z_zvezdica}"
        self.seznam = []
        
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


# vrstica 703, ne razumem zakaj si self.seznam zapomni rešitve iz prejšnega primera 
# da se ne bi podvajal ob vsakem pritisku na gumb sem zraven dodal števec, 
# ampak če okno "robustni problem nahrbtnika" zaprem s pritiskom na gumb "zapri" se števec ponastavi na 0 ampak
# self.seznam si pa zapomne kak je bil v prvem primeru