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
    
    # Dodajanje neodivisnega elementa + mal je treba še začetne pogoje spremenit v funkciji 
    # if len(N)//2 != len(N)/2:
    #     print(w,p,maks_w)
    #     w.append(1)
    #     p.append(0)
    #     maks_w.append(1)
    #     print(w,p, maks_w)

        if lamda is not None:
            if lamda > len(N):
                lamda = len(N)
                print("Lamda je večja kot moč množice predmetov, zato sva lamdo nastavila na", len(N))
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
                element = N[i - 1]
                set_stvari.append([element, w[i - 1], p[i - 1]])
                seznam_stvari.append(element)
                c_zvezdica += w[i - 1]
                z_zvezdica1 -= p[i - 1]
                c -= w[i - 1]
        return [seznam_stvari, z_zvezdica]

#solve_KP([1,2,3], 2, [1,1,1], [3,4,3])

# solve_eKkP vrne seznam vseh predmetov in optimalno vrednost, če dodatno omejimo maksimalno števio uporabljenih predmetov s k 
# rezulatat v smislu ([[4, 4, 3], [3, 6, 5]], 8), kar pomeni 4 predmet, teža = 4, vrednost 3 in 3 predmet, teža 6 in 5 vrednost.
def solve_eKkP(N, c, w, p, k):
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

# primer
#print(solve_eKkP([1, 2, 3, 4], 10,[2, 3, 6, 4], [1, 2, 5, 3], 2))
#print(solve_eKkP([1, 2, 3, 4], 10,[2, 3, 6, 4], [1, 2, 5, 3], 2))


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
                print(seznam)
                return(seznam)
            else: 
                print(seznam)
                return(seznam)
        else:
            if w[0] <= c_zvezdica:
                seznam.append(N[0])
                print(seznam)
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
            #z1_c_zvezdica = RKP(N1, c_zvezdica, w1, p1, lamda, maks_w1)[0]
            #z2_c_zvezdica = solve_KP(N2, c_zvezdica, w2, p2)[1] # tu ko boma dodala v RKP da naredi seznam še lahk kličema kr RKP
            for c_1 in range(c_zvezdica + 1):
                if c_1 == 0:
                    z1_c_1 = 0
                    z2_c_2 = solve_KP(N2, c_zvezdica, w2, p2)[1]                
                elif c_1 == c_zvezdica:
                    z2_c_2 = 0
                    z1_c_1 = RKP(N1, c_zvezdica, w1, p1, lamda, maks_w1)[0]
                else:
                    z1_c_1 = RKP(N1, c_1, w1, p1, lamda, maks_w1)[0]
                    z2_c_2 = solve_KP(N2, c_zvezdica - c_1, w2, p2)[1]
                    if z1_c_1 + z2_c_2 == z_zvezdica:
                        z2_c2 = z2_c_2
                        z1_c1 = z1_c_1
                        c1 = c_1
                        c2 = c_zvezdica - c1
            solution_set_kp = solve_KP(N2, c2, w2, p2)[0]
            seznam.append(solution_set_kp)
            k1_zvezdica = RKP(N1, c1, w1, p1, lamda, maks_w1)[3]
            return rekurzija(N1, z1_c1 , k1_zvezdica, c1, lamda, w1, maks_w1, p1, seznam)        
        else: 
            #z1_c_zvezdica = solve_eKkP(N1, c_zvezdica, maks_w1, p1, k_zvezdica)[1]
            #z2_c_zvezdica = RKP(N2, c_zvezdica, w2, p2, lamda - k_zvezdica, maks_w2)[0]
            for c_1 in range(c_zvezdica + 1):
                if c_1 == 0:
                    z1_c_1 = 0
                    z2_c_2 = RKP(N2, c_zvezdica, w2, p2, lamda - k_zvezdica, maks_w2)[0] 
                elif c_1 == c_zvezdica:
                    z2_c_2 = 0
                    z1_c_1 = solve_eKkP(N1, c_zvezdica, w1, p1, k_zvezdica)[1]                    
                else:
                    z2_c_2 = RKP(N2, c_zvezdica - c_1, w2, p2, lamda - k_zvezdica, maks_w2)[0]
                    z1_c_1 = solve_eKkP(N1, c_1, w1, p1, k_zvezdica)[1]
                    if z1_c_1 + z2_c_2 == z_zvezdica:
                        z2_c2 = z2_c_2
                        z1_c1 = z1_c_1
                        c1 = c_1
                        c2 = c_zvezdica - c1
            solution_set_eKkP = solve_eKkP(N1, c1, w1, p1, k_zvezdica)[0]
            seznam.append(solution_set_eKkP)
            k2_zvezdica = RKP(N2, c2, w2, p2, lamda - k_zvezdica, maks_w2)[3]
            return rekurzija(N2, z2_c2, k2_zvezdica, c2,lamda - k_zvezdica, w2, maks_w2, p2, seznam)
    

# rekurzija(N, z_zvezdica, k_zvezdica, c_zvezdica, lamda, w, maks_w, p)
kkk = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[3]
zzz = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[0]
ccc = RKP([1,2,3,4, 5], 9, [1,2,3,1, 2], [4,5,5,3, 2], 1, [3,3,3,3, 2])[1]
lamda = 1
N = [1,2,3,4, 5]
w = [1,2, 3, 1, 2]
maks_w = [3,3,3,3, 2]
p = [4,5,5,3, 2]
print(ccc)
print(zzz)
print(kkk)
print(podatki([1, 2, 3, 4, 5], [1, 2, 3, 1, 2], [4, 5, 5, 3, 2], [3, 3, 3, 3, 2]))
rekurzija(N, zzz, kkk, ccc, lamda, w, maks_w, p)
# RKP([6,3,1], 0, [1,1,1], [3,4,3], lamda, [3,3,3])
kkk, zzz, ccc = RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[3], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[0], RKP({1,2,3,4,5,6}, 10, [1,1,1,2,3,1], [2,3,4,5,5,3], 6, [3,3,3,3,3,3])[1]
lamda = 0
N = {1,2,3,4,5,6}
w = [1,1,1,2,3,1]
maks_w = [3,3,3,3,3,3]
p = [2,3,4,5,5,3]

# rekurzija(N, zzz, kkk, ccc, lamda, w, maks_w, p)
# RKP([6,3,1], 0, [1,1,1], [3,4,3], lamda, [3,3,3])



##### ČE ŠE NIMAŠ SI MOREŠ ZAGNAT TOLE V TERMINALU
# python3 -m pip install pillow v bash (terminal)

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
        self.komentar = tk.Label(self.frame, text= " napišite celo število, npr. 5 \n \n \n \n \n \n \n \n \n \n \n \n")
        self.quitButton = tk.Button(self.frame, text = 'Zapri', width = 5, command = self.close_windows)
        self.backButton = tk.Button(self.frame, text = 'Nazaj', width = 5, command = self.nazaj)
        self.stevilo_podatkov = tk.Entry(self.frame, width=20, selectborderwidth=2,bg= "gray90")
        self.prazno_polje = tk.Label(self.frame, text = '', width = 15)
        self.label1 = tk.Label(self.frame,text = "Koliko predmetov imate? ")
        self.prazno_polje1 = tk.Label(self.frame,text = "", width = 3)
        #self.prazno_polje2 = tk.Label(self.frame,text = "", height= 6)
        # slika
        image = Image.open("/Users/zaloznikjan/Desktop/fp/Robust-knapsack-problem/nahrbtnik.jpg")
        image = image.resize((250, 220), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.slika = tk.Label(self.frame, image=photo)
        self.slika.image = photo


        # prikaz
        #self.slika.grid(row=2,column=1)
        self.slika.place(x=205, y=50)
        #self.prazno_polje2.grid(row=3, column =0)
        self.komentar.grid(row=2, column=0)
        self.stevilo_podatkov.grid(row=1, column=0) 
        self.prazno_polje1.grid(row=2, column=2)
        self.prazno_polje.grid(row=1, column=1)
        self.label1.grid(row=0, column=0)
        self.backButton.grid(row=0, column=4)
        self.quitButton.grid(row=0, column=5)
        self.frame.grid()
        
        
    
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
        self.master.geometry("470x284+500+300")
        #gumbi 
        self.komentar = tk.Label(self.frame, text= " napišite celo število, npr. 5 \n \n \n \n \n \n \n \n \n \n \n \n")
        self.quitButton = tk.Button(self.frame, text = 'Zapri', width = 5, command = self.close_windows)
        self.backButton = tk.Button(self.frame, text = 'Nazaj', width = 5, command = self.nazaj)
        self.stevilo_podatkov = tk.Entry(self.frame, width=20, selectborderwidth=2,bg= "gray90")
        self.prazno_polje1= tk.Label(self.frame, text = '', width = 15)
        self.label1 = tk.Label(self.frame,text = "Koliko predmetov imate? ")
        self.prazno_polje2 = tk.Label(self.frame,text = "", width = 3)
        #self.prazno_polje2 = tk.Label(self.frame,text = "", height= 6)
        # slika
        image = Image.open("/Users/zaloznikjan/Desktop/fp/Robust-knapsack-problem/knapsack.png")
        image = image.resize((219, 219), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.slika1 = tk.Label(self.frame, image=photo)
        self.slika1.image = photo


        # prikaz
        #self.slika.grid(row=2,column=1)
        self.slika1.place(x=220, y=35)
        #self.prazno_polje2.grid(row=3, column =0)
        self.komentar.grid(row=2, column=0)
        self.stevilo_podatkov.grid(row=1, column=0) 
        self.prazno_polje2.grid(row=2, column=2)
        self.prazno_polje1.grid(row=1, column=1)
        self.label1.grid(row=0, column=0)
        self.backButton.grid(row=0, column=4)
        self.quitButton.grid(row=0, column=5)
        self.frame.grid()

    def nazaj(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PRVO_OKNO(self.newWindow)

    def close_windows(self):
        self.master.destroy()

def main(): 
    okno = tk.Tk()
    app1 = PRVO_OKNO(okno)
    okno.geometry("450x225+500+300")
    okno.title("Problem nahrbtnika")
    okno.mainloop()

if __name__ == '__main__':
     main()

# import tkinter as tk

# class PRVO_OKNO:
#     def __init__(self, master):
#         self.master = master
#         self.master.geometry("450x225+500+300")
#         self.frame = tk.Frame(self.master)
#         self.butnew("Window 1", "ONE", NAVADNI_PROBLEM)
#         self.butnew("Window 2", "TWO", ROBUSTNI_PROBLEM)
#         self.frame.pack()

#     def butnew(self, text, number, _class):
#         tk.Button(self.frame, text = text, width = 25, command = lambda: self.new_window(number, _class)).pack()

#     def new_window(self, number, _class):
#         self.newWindow = tk.Toplevel(self.master)
#         _class(self.newWindow, number)


# class NAVADNI_PROBLEM:
#     def __init__(self, master, number):
#         self.master = master
#         self.master.geometry("400x400+400+400")
#         self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
#         self.label = tk.Label(master, text=f"this is window number {number}")
#         self.label.pack()
#         self.quitButton.pack()
#         self.frame.pack()

#     def close_windows(self):
#         self.master.destroy()

# class ROBUSTNI_PROBLEM:
#     def __init__(self, master, number):
#         self.master = master
#         self.master.geometry("400x400+400+400")
#         self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
#         self.label = tk.Label(master, text=f"this is window number {number}")
#         self.label.pack()
#         self.label2 = tk.Label(master, text="THIS IS HERE TO DIFFERENTIATE THIS WINDOW")
#         self.label2.pack()
#         self.quitButton.pack()
#         self.frame.pack()

#     def close_windows(self):
#         self.master.destroy()




# def main(): 
#     root = tk.Tk()
#     app = PRVO_OKNO(root)
#     root.mainloop()

# if __name__ == '__main__':
#     main()


