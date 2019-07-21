import math
import random
import matplotlib.pyplot as plt
import time
import numpy



#Reaktionskontanten
c1 = 0.001
c2 = 0.1

#Anfangszustand
x = [499, 1, 0]
S = [x[0]]
I = [x[1]]
R = [x[2]]

#Zeit
t = 0.0
time = [t]

while x[0] != 0 or x[2] == 500:
    #Berechnung der Ratenfunktionen
    a1 = x[0] * x[1] * c1
    a2 = x[1] * c2
    a0 = a1 + a2
    if a0 == 0:
        break
    #Sample von tau
    r1 = random.uniform(0.0, 1.0)
    tau = numpy.random.exponential(1 / a0)
    t = t + tau
    time.append(t)

    #Entscheidung welche reaktion stattfindet
    if random.uniform(0.0, 1.0) < a1 / a0:
        x[0] = x[0] - 1
        x[1] = x[1] + 1
    else:
        x[1] = x[1] - 1
        x[2] = x[2] + 1
    S.append(x[0])
    I.append(x[1])
    R.append(x[2])

plt.plot(time, S)
plt.plot(time, I)
plt.plot(time, R)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S', 'I', 'R'))
plt.show()



