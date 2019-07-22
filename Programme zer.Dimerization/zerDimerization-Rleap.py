import numpy
import math
import matplotlib.pyplot as plt

#Matrix mit stöchiometrischen vektoren
V = [[-1, -2, 1, 0], [0, 1, -1, -1], [0, 0, 0, 1]]

#Reaktionskonstanten
c = [1, 0.002, 0.5, 0.04]

#Nutzerdefinierte Parameter
epsilon = 0.03
theta = 0.1
#Indicemenge mit reagierenden Spezies
Irs = [0, 1]

#Anfangszustand
x = [10**5, 1, 1]
S1 = [x[0]]
S2 = [x[1]]
S3 = [x[2]]

#Zeit
t = 0.0
time = [t]
Tend = 10

while t < Tend:
    #Höchster Grad der Reaktion
    g = [2 + (1 / (x[0] - 1)), 1]

    #Berechnung der Ratenfunktionen
    a1 = x[0] * c[0]
    a2 = 1 / 2 * x[0] * (x[0] - 1) * c[1]
    a3 = x[1] * c[2]
    a4 = x[1] * c[3]
    a = [a1, a2, a3, a4]
    a0 = sum(a)
    MaxRec = [x[0], math.floor(x[0] / 2), x[1], x[1]]

    #Berechnung der Gesamt-Anzahl an Reaktionen
    u = [0, 0]
    o = [0, 0]
    temp = [0, 0]
    for i in Irs:
        for j in [0, 1, 2, 3]:
            u[i] = u[i] + V[i][j] * a[j]
            o[i] = o[i] + (V[i][j] ** 2) * a[j]
        temp[i] = min((max(epsilon * x[i] / g[i], 1)) / (abs(u[i])),
                      ((max(epsilon * x[i] / g[i], 1)) ** 2) / (abs(o[i]) - abs(((u[i]) ** 2) / a0)))
    L1 = math.floor(a0 * min(temp))

    #Behebungsmechanismus gegen negative Spezies
    temp = []
    for i in [0, 1, 2, 3]:
        temp.append(1 - theta * (1 - (a0 / a[i])) * MaxRec[i])
    L2 = math.floor(min(temp))
    L = min(L1, L2)

    #Sample von tauL
    tau = numpy.random.gamma(L, 1 / a0)

    #Sampleverfahren
    sample = [0, 0, 0, 0]
    sample[0] = numpy.random.binomial(L - sum(sample), a[0] / a0)
    sample[1] = numpy.random.binomial(L - sum(sample), a[1] / (a0 - a[0]))
    sample[2] = numpy.random.binomial(L - sum(sample), a[2] / (a0 - a[0] - a[1]))
    sample[3] = L - sum(sample)

    #Update Zeit und Zustand
    t = t + tau
    x[0] = x[0] - sample[0] - 2 * sample[1] + 2 * sample[2]
    x[1] = x[1] + sample[1] - sample[2] - sample[3]
    x[2] = x[2] + sample[3]
    time.append(t)
    S1.append(x[0])
    S2.append(x[1])
    S3.append(x[2])

plt.plot(time, S1, ':')
plt.plot(time, S2,  ':')
plt.plot(time, S3, ':')
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S1', 'S2', 'S3'))
plt.show()