from collections import Counter
def portfeljski_KP(c, n, N, p, w):
    z = [0 for i in range(c + 1)]
 
    seznam = [0 for i in range(c + 1)]
    for i in range(c + 1):
        for j in range(1, n + 1):
            if (w[j - 1] <= i):
                z[i] = max(z[i], z[i - w[j - 1]] + p[j - 1])
                if z[i] == z[i - w[j - 1]] + p[j - 1]:
                    seznam[i] = (j)
  #  zacasne_teze = []
   # zacasne_vrednosti = []
    #for el in seznam:
     #   zacasne_teze.append(w[int(el) - 1])
      #  zacasne_vrednosti.append(p[int(el) - 1])

    z_zvezdica = z[c]
    #z_zvezdica1 = z[c]
    #c_zvezdica = 0
    #seznam_stvari = []
    #for i in range(n + 1, 1, -1):
     #   if z_zvezdica1 <= 0:
        #    break
        #if z_zvezdica1 == z[c]:
         #   element = i
          #  seznam_stvari.append(element)
           # c_zvezdica += zacasne_teze[i - 1]
            #z_zvezdica1 -= zacasne_vrednosti[i - 1]
            #c -= zacasne_teze[i - 1]                
                   
    #stevec = Counter()
    #for el in seznam:
      #  stevec[el + 1] +=1
   # stvari = []
    #for el in seznam_stvari:
     #   stvari.append(seznam[el])
   
    return z_zvezdica