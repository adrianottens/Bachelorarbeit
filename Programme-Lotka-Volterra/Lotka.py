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

#Anfangspopulation
x = [1000, 1000, 0]
Prey = [x[0]]
Predator = [x[1]]
death = [x[2]]

#Zeit
t = 0.0
time = [t]

n = 0
while t < Tend:
    n = n + 1
    a1 = x[0] * c1
    a2 = x[0] * x[1] * c2
    a3 = x[1] * c3

    a = [a1, a2, a3]
    a0 = sum(a)
    if a0 == 0:
        break
    tau = numpy.random.exponential(1 / a0)
    t = tau + t
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

#Anzahl der Schritte
print(n)

plt.plot(time, Prey)
plt.plot(time, Predator)
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('Beute', 'Räuber'))
plt.show()
