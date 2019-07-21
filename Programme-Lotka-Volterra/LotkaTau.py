import numpy
import math
import matplotlib.pyplot as plt

#Endzeit
Tend = 10

#Reaktionskonstanten
c1 = 10
c2 = 0.01
c3 = 10

#Metrix mit den stöchiometrischen Vektoren
v = [[1, -1, 0], [0, 1, -1], [0, 0, 1]]

#Nutzer-definierte Parameter
nc = 10
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
time = [t]

n = 0

while t < Tend:
    #Berechnung der Ratenfunktionen
    a1 = x[0] * c1
    a2 = x[0] * x[1] * c2
    a3 = x[1] * c3
    a = [a1, a2, a3]
    a0 = sum(a)

    #Unterteilung in kritischen und nicht kritischen Reaktionen
    NonCrit = []
    Crit = []
    #Maximaleanzahl an möglichen Reaktionen
    MaxReaction = [math.inf, x[0], x[1]]
    for i in [0, 1, 2]:
        if MaxReaction[i] < nc:
            Crit.append(i)
        else:
            NonCrit.append(i)
    if Crit == 0:
        print(Crit)
    #Berechnung von tau1
    temp = [0, 0, 0, 0]
    for i in Irs:
        for j in NonCrit:
            temp[i] = temp[i] + v[i][j] * a[j]
            temp[i+2] = temp[i+2] + (v[i][j])**2 * a[j]

    if all(temp) == 0:
        tau = numpy.random.exponential(1/a0)
    else:
        tau = min(max(eps*x[0]/g[0], 1)/abs(temp[0]), max(eps*x[1]/g[1], 1)/abs(temp[1]),
                  max(eps*x[0]/g[0], 1)**2/abs(temp[2]), max(eps*x[1]/g[1], 1)**2/abs(temp[3]))

    #falls kleiner als erwartete Schrittweite im SSA, 100 SSA Schritte
    if tau < 1/a0:
        m = 0
        while m != 100:
            a1 = x[0] * c1
            a2 = x[0] * x[1] * c2
            a3 = x[1] * c3
            a = [a1, a2, a3]
            a0 = sum(a)
            tau = numpy.random.exponential(1/a0)
            t = t + tau
            temp = numpy.random.uniform(0.0, 1.0)
            if temp < a1 / a0:
                x[0] = x[0] + 1
            elif temp < (a1 + a2) / a0:
                x[0] = x[0] - 1
                x[1] = x[1] + 1
            else:
                x[1] = x[1] - 1
                x[2] = x[2] + 1
            Prey.append(x[0])
            Predator.append(x[1])
            death.append(x[2])
            time.append(t)
            if t < Tend:
                break
            m = m + 1
        n = n + m

    else:
        #Berechnung der Zeit bis zur nächsten kritischen reaktion, i.e tau2
        sample = [0, 0, 0]
        ac0 = 0
        for j in Crit:
            ac0 = ac0 + a[j]
        if ac0 == 0:
            tau2 = math.inf
        else:
            tau2 = numpy.random.exponential(1/ac0)
        #Vergleich und Sample-Ziehung
        if tau < tau2:
            for i in NonCrit:
                sample[i] = numpy.random.poisson(tau*a[i])
        else:
            tau = tau2
            for i in NonCrit:
                sample[i] = numpy.random.poisson(tau*a[i])
            temp = numpy.random.uniform(0.0, 1.0)
            temp2 = 0
            if len(Crit) == 1:
                sample[Crit[0]] = 1
            else:
                temp = numpy.random.uniform(0.0, 1.0)
                if temp < a[Crit[0]]/ac0:
                    jc = Crit[0]
                else:
                    jc = Crit[1]
                sample[jc] = 1
        #update der Zustände und der Zeit
        x[0] = x[0] + sample[0] - sample[1]
        x[1] = x[1] + sample[1] - sample[2]
        x[2] = x[2] + sample[2]
        Prey.append(x[0])
        Predator.append(x[1])
        death.append(x[2])
        t = t + tau
        time.append(t)
        n = n + 1

#Anzahl der Schritte
print(n)
plt.plot(time, Prey)
plt.plot(time, Predator)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('Beute', 'Räuber'))
plt.show()
plt.show()
