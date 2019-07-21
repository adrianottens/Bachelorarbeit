import numpy
import math
import matplotlib.pyplot as plt
#Nutzerdefinierte Parameter
epsilon = 0.01
nc = 10

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
while x[2] != 500 or x[1] == 0:
    #Berechnung der Ratenfunktionen
    a1 = c1 * x[0] * x[1]
    a2 = c2 * x[1]
    a = [a1, a2]
    a0 = sum(a)
    if a0 == 0.0:
        break
    #Unterteilung in kritische und nicht kritische Reaktionen
    MaxReaction = [x[0], x[1]]
    Critical = []
    Noncritical = []
    for i in [0, 1]:
        if MaxReaction[i] < nc:
            Critical.append(i)
        else:
            Noncritical.append(i)
    #Berechnung von tau1
    u = [0, 0]
    o = [0, 0]
    temp = [0, 0, 0, 0]

    for i in Irs:
        for j in Noncritical:
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
    #Berechnung von tau2
    ac0 = 0
    for i in Critical:
        ac0 = ac0 + a[i]
    if ac0 == 0:
        tau2 = 1000
    else:
        tau2 = numpy.random.exponential(1 / ac0)
    sample = [0, 0]
    #Vergleich der tau und samplen
    if tau < tau2:
        for j in Noncritical:
            sample[j] = numpy.random.poisson(a[j] * tau)
        for i in Critical:
            sample[i] = 0
    else:
        tau = tau2
        r = numpy.random.uniform(0.0, 1.0)
        temp = a[Critical[0]]
        for i in Critical:
            if r < a[i] / ac0:
                sample[i] = 1
            else:
                sample[i] = 0
        for j in Noncritical:
            sample[j] = numpy.random.poisson(a[j] * tau)

    #update der Zustände und Zeit
    x[0] = x[0] - sample[0]
    x[1] = x[1] + sample[0] - sample[1]
    x[2] = x[2] + sample[1]
    S.append(x[0])
    I.append(x[1])
    R.append(x[2])
    t = t + tau
    time.append(t)
    n = n + 1
#Anzahl der Schritte
print(n)

plt.plot(time, S)
plt.plot(time, I)
plt.plot(time, R)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S', 'I', 'R'))
plt.show()



