import numpy
import math
import matplotlib.pyplot as plt

#Matrix mit stöchiometrische Vektoren
V = [[-1, -2, 1, 0], [0, 1, -1, -1], [0, 0, 0, 1]]

#Reaktionskonstanten
c = [1, 0.002, 0.5, 0.04]

#Nutzer-definierte Parameter
epsilon = 0.03
nc = 10

#Indicemenge der reagierenden Spezies
Irs = [0, 1]

#Zeit
Tend = 10
t = 0.0
time = [t]

#Anfangszustand
x = [10**5, 0, 0]
S1 = [x[0]]
S2 = [x[1]]
S3 = [x[2]]

n = 0
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

    #Unterscheidung zwischen kritischen und nicht-kritischen Reaktionen
    MaxRec = [x[0], math.floor(x[0] / 2), x[1], x[1]]
    Crit = []
    nCrit = []
    for i in [0, 1, 2, 3]:
        if MaxRec[i] < nc:
            Crit.append(i)
        else:
            nCrit.append(i)
    #Berechnug von tau1
    u = [0, 0]
    o = [0, 0]
    temp = [0, 0]
    for i in Irs:
        for j in nCrit:
            u[i] = u[i] + V[i][j] * a[j]
            o[i] = o[i] + (V[i][j] ** 2) * a[j]
        temp[i] = min((max(epsilon * x[i] / g[i], 1)) / (abs(u[i])),
                      ((max(epsilon * x[i] / g[i], 1)) ** 2) / (abs(o[i])))
    tau1 = min(temp)
    #Falls tau1 kleiner als die erwartete Schrittweite im SSA, 100 SSA schritte
    if tau1 < 10 / a0:
        d = 0
        while d != 100:
            n = n + 1
            a1 = x[0] * c[0]
            a2 = 1 / 2 * x[0] * (x[0] - 1) * c[1]
            a3 = x[1] * c[2]
            a4 = x[1] * c[3]
            a = [a1, a2, a3, a4]
            a0 = sum(a)
            tau = numpy.random.exponential(1 / a0)
            t = t + tau
            temp = numpy.random.uniform(0.0, 1.0)
            if temp < a[0] / a0:
                x[0] = x[0] - 1
            elif temp < (a[0] + a[1]) / a0:
                x[0] = x[0] - 2
                x[1] = x[1] + 1
            elif temp < (a[0] + a[1] + a[2]) / a0:
                x[0] = x[0] + 2
                x[1] = x[1] - 1
            else:
                x[1] = x[1] - 1
                x[2] = x[2] + 1
            time.append(t)
            S1.append(x[0])
            S2.append(x[1])
            S3.append(x[2])
            d = d + 1
    else:
        sample = [0, 0, 0, 0]
        #berechnung von tau2, zeit zur nächsten kritischen Reaktion
        ac0 = 0
        for i in Crit:
            ac0 = ac0 + a[i]
        if ac0 == 0:
            tau2 = math.inf
        else:
            tau2 = numpy.random.exponential(1 / ac0)
        #Vergleich der taus und samplen der Reaktionsanzahl
        if tau1 <= tau2:
            tau = tau1
            for i in nCrit:
                sample[i] = numpy.random.poisson(a[i] * tau)
        else:
            tau = tau2
            r = numpy.random.uniform(0.0, 1.0)
            temp = 0
            for j in Crit:
                temp = temp + a[j]
                if r < temp / ac0:
                    sample[j] = 1
            for i in nCrit:
                sample[i] = numpy.random.poisson(a[i] * tau)
        #Update von zustand und Zeit
        t = t + tau
        x[0] = x[0] - sample[0] - 2 * sample[1] + 2 * sample[2]
        x[1] = x[1] + sample[1] - sample[2] - sample[3]
        x[2] = x[2] + sample[3]
        time.append(t)
        S1.append(x[0])
        S2.append(x[1])
        S3.append(x[2])
        n = n + 1

#Anzahl der Schritte
print(n)

plt.plot(time, S1, ':')
plt.plot(time, S2,  ':')
plt.plot(time, S3, ':')
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S1', 'S2', 'S3'))
plt.show()