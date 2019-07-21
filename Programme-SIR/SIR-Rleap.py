import numpy
import math
import matplotlib.pyplot as plt
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
while x[2] != 500 or x[1] != 0:
    n = n + 1
    #Berechnung der Ratenfunktionen
    a1 = c1 * x[0] * x[1]
    a2 = c2 * x[1]
    a = [a1, a2]
    a0 = sum(a)

    MaxReaction = [min(x[0], x[1]), x[1]]
    if a0 == 0.0:
        break
    #Berechnung von der Anzahl an Reaktionen L
    u = [0, 0]
    o = [0, 0]
    temp = [0, 0, 0, 0]
    for i in Irs:
        for j in [0, 1]:
            u[i] = u[i] + v[i][j] * a[j]
            o[i] = o[i] + (v[i][j]) ** 2 * a[j]
    sample = [0, 0]
    if all(u) == 0 or all(o) == 0:
        L = 1
    else:
        temp = min(max(epsilon * x[0] / g[0], 1) / (abs(u[0])), max(epsilon * x[1] / g[1], 1) / (abs(u[1])))
        temp2 = min(max(epsilon * x[0] / g[0], 1) ** 2 / (o[0] - (u[0] ** 2 / a0)),
                    max(epsilon * x[1] / g[1], 1) ** 2 / (o[1] - (u[1] ** 2 / a0)))
        L = math.floor(a0 * min(temp, temp2))
        #Behebungsmechanismus gegen negative Spezies
        Lbar = math.floor(
            min((1 - teta * (1 - (a0 / a[0]))) * MaxReaction[0], (1 - teta * (1 - (a0 / a[1]))) * MaxReaction[1]))
        L = min(L, Lbar)
    #Sample für tauL
    tau = numpy.random.gamma(L, 1 / a0)
    sample = [0, 0]
    #Sample aus den binomialvariablen
    sample[0] = numpy.random.binomial(L, a[0] / a0)
    sample[1] = L - sample[0]
    #Update vom Zustand und Zeit
    x[0] = x[0] - sample[0]
    x[1] = x[1] + sample[0] - sample[1]
    x[2] = x[2] + sample[1]
    S.append(x[0])
    I.append(x[1])
    R.append(x[2])
    t = t + tau
    time.append(t)

#Anzahl an Schritte
print(n)

plt.plot(time, S)
plt.plot(time, I)
plt.plot(time, R)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S', 'I', 'R'))
plt.show()

