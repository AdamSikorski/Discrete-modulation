import math
import numpy as np
import matplotlib.pyplot as plt

"""
5 podpunkt:
W = max - min
W = 0  dla ka¿dego sygna³u.
"""

switch = bool() # True -> little endian, False -> big endian

def S2BS( napis, switch ):

  if( switch == True ): # little endian
    b = [bin(ord(x))[2:].zfill(8) for x in napis]
    global zwracana_wartosc
    for x in b:
      #print (x)
      zwracana_wartosc = "".join(b)
    print(zwracana_wartosc)
    return (zwracana_wartosc)

  if( switch == False ): # big endian
    b = [bin(ord(x))[2:].zfill(8) for x in napis]
    global zwracana_wartoscc
    zwracana_wartoscc = ""
    for x in b:
      def reverse(s): 
        str = "" 
        for i in s: 
          str = i + str
        return str
      reverse(x)
      zwracana_wartoscc += reverse(x)
    print(zwracana_wartoscc)
    
print("Little endian: ")
S2BS('KOT',True)

print('\n')

print("Big endian: ")
S2BS('KOT',False)

tablica_na_wartosci = []

for i in range(0,len(zwracana_wartosc),1):
  if zwracana_wartosc[i] == '0':
    tablica_na_wartosci.append(0)
  if zwracana_wartosc[i] == '1':
    tablica_na_wartosci.append(1)

co_wyswietlic = int(input("\nCo chcesz wyswietlic?\n(0-> Strumien bitowy, ASK -> 1, FSK -> 2, PSK -> 3): "))

if co_wyswietlic == 0:
  N = 2
  f = 9
  Tb = 1/f
  dt = 1.0/1000
  t0 = 0
  TN = Tb 
  n = 0
  tn = t0 + (n * dt)

  tab1 = []
  tab2 = []

  for i in range(0,len(tablica_na_wartosci), 1):
    while tn < TN:
        tab1.append(tn)
        tab2.append(zwracana_wartosc[i])
        n = n+1
        tn = t0 + (n*dt)
    TN += Tb

  plt.plot(tab1,tab2)
  plt.title('sygna³ informacyjny m(t)')
  plt.xlabel('Tb(s)')
  plt.ylabel('A')
  plt.show()
  plt.savefig('strumien bitowy.png')


if co_wyswietlic == 1:
  
  N = 2
  f = 9
  Tb = 1/f
  dt = 1.0/1000
  t0 = 0
  TN = Tb 
  n = 0
  tn = t0 + (n * dt)
  
  switchh = bool()
  def Za(switchh):
    if switchh == True: 
      A1 = 0
      fi = 0 
      wynik1 = A1 * (math.sin(2 * math.pi * f  * tn + fi))
      return wynik1
    if switchh == False: 
      A2 = 1
      fi = 0
      wynik2 = A2 * (math.sin(2 * math.pi * f  * tn + fi))
      return wynik2

  ograniczenie_bitow = 0  
  tab1 = []
  tab2 = []

  for i in range(0,len(tablica_na_wartosci), 1):
    while tn < TN:
      if tablica_na_wartosci[i] == 0:
        tab1.append(tn)
        tab2.append(Za(True))
        n = n+1
        tn = t0 + (n*dt)
      if tablica_na_wartosci[i] == 1:
        tab1.append(tn)
        tab2.append(Za(False))
        n = n+1
        tn = t0 + (n*dt)     
    TN += Tb
    ograniczenie_bitow +=1
    if ograniczenie_bitow == 10:
      break
  """  
  plt.plot(tab1,tab2)
  plt.title('kluczowanie amplitudy (ASK)')
  plt.xlabel('Tb(s)')
  plt.ylabel('A')
  plt.show()
  plt.savefig('ASK.png')
  """
  
  fs = 250
  N = len(tab2)
  x = np.zeros((N,)) 
  t = np.zeros((N,))
  X_re = np.zeros(N) 
  X_im = np.zeros(N) 
  M = np.zeros(N)
  f_k = np.zeros(N)
  
  def DFT():
    for k in range(0,N,1):
      for n in range(0,N,1):
        X_re[k] = X_re[k] + (tab2[n]*math.cos((-2*math.pi*k*n)/N))
        X_im[k] = X_im[k] + (tab2[n]*math.sin((-2*math.pi*k*n)/N))
    
    for k in range(0,N,1): 
      M[k] = math.sqrt(X_re[k] * X_re[k] + X_im[k] * X_im[k])
      M[k] = (M[k]*2)/N
      f_k[k] = k *(fs/N) 
      #print(f_k[k],M[k])
    
    treshhold = abs(max(M)) / 10000

    for k in range(0,N,1):
      if M[k] < treshhold:
        M[k] = 0 
        continue
      M[k] = 10 * math.log10(M[k])
   
    max_value = f_k[0]
    
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any()and (f_k[i] > max_value).any():
        max_value = f_k[i]
      
    min_value = f_k[int(N/2)]
   
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any() and (f_k[i] < min_value).any():
        min_value = f_k[i]

    wartosc = max_value - min_value
    if wartosc > 0:
      print("max - min = ",wartosc)
    if wartosc <=0:
      wartosc = 0
      print("max - min = ",wartosc)
    


  DFT()
  
  plt.bar(f_k[0:100],M[0:100],width = 0.1)
  plt.title('Widmo decybelowe ASK')
  plt.xlabel('f')
  plt.ylabel('A')
  plt.show()
  plt.savefig('widmo ASK.png')
  


if co_wyswietlic == 2:

  N = 2
  f = 9
  Tb = 1/f
  dt = 1.0/1000
  t0 = 0
  TN = Tb 
  n = 0
  tn = t0 + (n * dt)
  f1 = (N+1) / Tb
  f2 = (N+2) / Tb

  def Zf(switchh):
    if switchh == True: 
      A = 1
      fi = 0
      wynik1 = A * (math.sin(2 * math.pi * f1  * tn + fi))
      return wynik1
    if switchh == False: 
      A = 1
      fi = 0
      wynik2 = A * (math.sin(2 * math.pi * f2  * tn + fi))
      return wynik2

  ograniczenie_bitow = 0
  tab1 = []
  tab2 = []

  for i in range(0,len(tablica_na_wartosci), 1):
    while tn < TN:
      if tablica_na_wartosci[i] == 0:
        tab1.append(tn)
        tab2.append(Zf(True))
        n = n+1
        tn = t0 + (n*dt)
      if tablica_na_wartosci[i] == 1:
        tab1.append(tn)
        tab2.append(Zf(False))
        n = n+1
        tn = t0 + (n*dt)     
    TN += Tb
    ograniczenie_bitow +=1
    if ograniczenie_bitow == 10:
      break
  """
  plt.plot(tab1,tab2)
  plt.title('kluczowanie czêstotliwoœci (FSK)')
  plt.xlabel('Tb(s)')
  plt.ylabel('A')
  plt.show()
  plt.savefig('FSK.png')      
  """
  fs = 250
  N = len(tab2)
  x = np.zeros((N,)) 
  t = np.zeros((N,))
  X_re = np.zeros(N) 
  X_im = np.zeros(N) 
  M = np.zeros(N)
  f_k = np.zeros(N)
  

  def DFT():
    for k in range(0,N,1):
      for n in range(0,N,1):
        X_re[k] = X_re[k] + (tab2[n]*math.cos((-2*math.pi*k*n)/N))
        X_im[k] = X_im[k] + (tab2[n]*math.sin((-2*math.pi*k*n)/N))
    
    for k in range(0,N,1): 
      M[k] = math.sqrt(X_re[k] * X_re[k] + X_im[k] * X_im[k])
      M[k] = (M[k]*2)/N
      f_k[k] = k *(fs/N) 
      #print(f_k[k],M[k])
    
    treshhold = abs(max(M)) / 10000

    for k in range(0,N,1):
      if M[k] < treshhold:
        M[k] = 0 
        continue
      M[k] = 10 * math.log10(M[k])
   
    max_value = f_k[0]
    
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any()and (f_k[i] > max_value).any():
        max_value = f_k[i]
      
    min_value = f_k[int(N/2)]
   
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any() and (f_k[i] < min_value).any():
        min_value = f_k[i]

    wartosc = max_value - min_value
    if wartosc > 0:
      print("max - min = ",wartosc)
    if wartosc <=0:
      wartosc = 0
      print("max - min = ",wartosc)
    

  DFT()
  plt.bar(f_k[0:100],M[0:100],width = 0.1)
  plt.title('Widmo decybelowe FSK')
  plt.xlabel('f')
  plt.ylabel('A')
  plt.show()
  plt.savefig('widmo FSK.png')
  

if co_wyswietlic == 3:
  N = 2
  f = 9
  Tb = 1/f
  dt = 1.0/1000
  t0 = 0
  TN = Tb 
  n = 0
  tn = t0 + (n * dt)
  f1 = (N+1) / Tb
  f2 = (N+2) / Tb

  def Zp(switchh):
    if switchh == True: 
      A = 1
      fi1 = 0 
      wynik1 = A * (math.sin(2 * math.pi * f  * tn + fi1))
      return wynik1
    if switchh == False: 
      A = 1
      fi2 = math.pi
      wynik2 = A * (math.sin(2 * math.pi * f  * tn + fi2))
      return wynik2

  ograniczenie_bitow = 0
  tab1 = []
  tab2 = []

  for i in range(0,len(tablica_na_wartosci), 1):
    while tn < TN:
      if tablica_na_wartosci[i] == 0:
        tab1.append(tn)
        tab2.append(Zp(True))
        n = n+1
        tn = t0 + (n*dt)
      if tablica_na_wartosci[i] == 1:
        tab1.append(tn)
        tab2.append(Zp(False))
        n = n+1
        tn = t0 + (n*dt)     
    TN += Tb
    ograniczenie_bitow +=1
    if ograniczenie_bitow == 10:
      break
  """      
  plt.plot(tab1,tab2)
  plt.title('kluczowanie fazy (PSK)')
  plt.xlabel('Tb(s)')
  plt.ylabel('A')
  plt.show()
  plt.savefig('PSK.png')
  """
  
  fs = 250
  N = len(tab2)
  x = np.zeros((N,)) 
  t = np.zeros((N,))
  X_re = np.zeros(N) 
  X_im = np.zeros(N) 
  M = np.zeros(N)
  f_k = np.zeros(N)


  def DFT():
    for k in range(0,N,1):
      for n in range(0,N,1):
        X_re[k] = X_re[k] + (tab2[n]*math.cos((-2*math.pi*k*n)/N))
        X_im[k] = X_im[k] + (tab2[n]*math.sin((-2*math.pi*k*n)/N))
    
    for k in range(0,N,1): 
      M[k] = math.sqrt(X_re[k] * X_re[k] + X_im[k] * X_im[k])
      M[k] = (M[k]*2)/N
      f_k[k] = k *(fs/N) 
      #print(f_k[k],M[k])
    
    treshhold = abs(max(M)) / 10000

    for k in range(0,N,1):
      if M[k] < treshhold:
        M[k] = 0 
        continue
      M[k] = 10 * math.log10(M[k])
   
    max_value = f_k[0]
    
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any()and (f_k[i] > max_value).any():
        max_value = f_k[i]
      
    min_value = f_k[int(N/2)]
   
    for i in range(0,int(N/2),1):
      if (M[i]>=-3).any() and (M[i] != 0).any() and (f_k[i] < min_value).any():
        min_value = f_k[i]

    wartosc = max_value - min_value
    if wartosc > 0:
      print("max - min = ",wartosc)
    if wartosc <=0:
      wartosc = 0
      print("max - min = ",wartosc)
    

  DFT()

  plt.bar(f_k[0:100],M[0:100],width = 0.1)
  plt.title('Widmo decybelowe PSK')
  plt.xlabel('f')
  plt.ylabel('A')
  plt.show()
  plt.savefig('widmo PSK.png')
  
