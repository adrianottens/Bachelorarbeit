import numpy
import math
import matplotlib.pyplot as plt
import time
#Endzeit
Tend = 10

#Reaktionskonstanten
c1 = 10
c2 = 0.01
c3 = 10

#Metrix mit den stöchiometrischen Vektoren
v = [[1, -1, 0], [0, 1, -1], [0, 0, 1]]

#Nutzer-definierte Parameter
theta = 10
eps = 0.03

#Indicesmenge für die in den Reaktionen involvierte Spezies
Irs = [0, 1]
#höchster Grad an Reaktion
g = [2, 2]

#Anfangspopulation
x = [1000, 1000, 0]
Predator = [x[1]]
Prey = [x[0]]
death = [x[2]]

#Zeit
t = 0.0
times = [t]

n = 0

while t < Tend:
    #Berechnung der Ratenfunktionen
    a1 = x[0] * c1
    a2 = x[0] * x[1] * c2
    a3 = x[1] * c3
    a = [a1, a2, a3]
    a0 = sum(a)
    #Berechnung der Anzahl an Reaktionen L
    MaxReaction = [math.inf, x[0], x[1]]
    temp = [0, 0, 0, 0]
    for i in Irs:
        for j in [0, 1, 2]:
            temp[i] = temp[i] + v[i][j] * a[j]
            temp[i + 2] = temp[i + 2] + (v[i][j]) ** 2 * a[j]
    if all(temp) == 0:
        L = 1
    else:
        L = math.floor(a0 * min(max(eps * x[0] / g[0], 1) / abs(temp[0]), max(eps * x[1] / g[1], 1) / abs(temp[1]),
                                max(eps * x[0] / g[0], 1) ** 2 / (temp[2] - abs(temp[0] ** 2 / a0)),
                                max(eps * x[1] / g[1], 1) ** 2 / (temp[3] - abs(temp[1] ** 2 / a0))))
    #zweite Wahl von L für das vermeiden negativer Spezies
    Lbar = min(MaxReaction[1] * (1 - theta * (1 - (a0 / a[1]))), MaxReaction[2] * (1 - theta * (1 - (a0 / a[2]))))
    L = min(L, Lbar)
    #Sample des Zeitschrittes tauL
    tau = numpy.random.gamma(L, 1 / a0)
    #Sample aus den korrelierten binomial verteilten Variablen
    sample = [0, 0, 0]
    sample[0] = numpy.random.binomial(L, a[0] / a0)
    sample[1] = numpy.random.binomial(L - sample[0], a[1] / (a0 - a[0]))
    sample[2] = L - sum(sample)
    #Update Zustand und Zeit
    x[0] = x[0] + sample[0] - sample[1]
    x[1] = x[1] + sample[1] - sample[2]
    x[2] = x[2] + sample[2]
    Prey.append(x[0])
    Predator.append(x[1])
    death.append(x[2])
    t = t + tau
    times.append(t)
    n = n + 1

#Anzahl der benötigten Schritte
print(n)
plt.plot(times, Prey)
plt.plot(times, Predator)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('Beute', 'Räuber'))
plt.show()


