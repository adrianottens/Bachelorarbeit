import numpy
import math
import matplotlib.pyplot as plt
import time
#Nutzerdefinierte Parameter
epsilon = 0.03
teta = 0.1

#Matrix mit stöchiometrische Vektoren
v = [[-1, 0], [1, -1], [0, 1]]

#Indicemenge mit reagiereden Spezies und höchster Grad an Reaktion
Irs = [0, 1]
g = [2, 1]

#Reaktionskonstanten
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

n = 0
while x[1] != 0 or x[2] != 500:
    #Berechnung der Ratenfunktionen
    a1 = c1 * x[0] * x[1]
    a2 = c2 * x[1]
    a = [a1, a2]
    a0 = sum(a)
    MaxReaction = [min(x[0], x[1]), x[1]]
    if a0 == 0:
        break
    #Berechnung von tau
    u = [0, 0]
    o = [0, 0]
    temp = [0, 0, 0, 0]
    for i in Irs:
        for j in [0, 1]:
            u[i] = u[i] + v[i][j] * a[j]
            o[i] = o[i] + (v[i][j]) ** 2 * a[j]
    sample = [0, 0]
    if all(u) == 0 or all(o) == 0:
        tau = numpy.random.exponential(1 / a0)
    else:
        for i in Irs:
            temp[i] = (max((epsilon * x[i]) / g[i], 1)) / (abs(u[i]))
            temp[i + 2] = (max((epsilon * x[i]) / g[i], 1)) ** 2 / (o[i])
        tau = min(temp)
    #Sample für Anzahl an Gesamt-Reaktionen L
    L = numpy.random.poisson(a0 * tau)
    if L == 0:
        t = t + tau
        L = 1
        tau = numpy.random.exponential(1 / a0)
    #Behebungsmechanismus aus dem R-leap
    Lbar = math.floor(
        min((1 - teta * (1 - (a0 / a[0]))) * MaxReaction[0], (1 - teta * (1 - (a0 / a[1]))) * MaxReaction[1]))

    L = min(L, Lbar)
    #Sample aus binomial Variablen
    sample = [0, 0]
    sample[0] = numpy.random.binomial(L, a[0] / a0)
    sample[1] = L - sample[0]
    #Update der Zustände und der Zeit
    x[0] = x[0] - sample[0]
    x[1] = x[1] + sample[0] - sample[1]
    x[2] = x[2] + sample[1]
    S.append(x[0])
    I.append(x[1])
    R.append(x[2])
    t = t + tau
    time.append(t)
    n = n + 1
#Anzahl an Schritte
print(n)

plt.plot(time, S)
plt.plot(time, I)
plt.plot(time, R)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S', 'I', 'R'))
plt.show()

