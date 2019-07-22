import numpy
import matplotlib.pyplot as plt

#Matrix mit stöchiometrischen Vektoren
V = [[-1, -2, 1, 0], [0, 1, -1, -1], [0, 0, 0, 1]]
#Reaktionskonstanten
c = [1, 0.002, 0.5, 0.04]

#Anfangszustand
x = [10**5, 0, 0]
S1 = [x[0]]
S2 = [x[1]]
S3 = [x[2]]

#Zeit
t = 0.0
time = [t]
Tend = 10

n = 0
while t < Tend:
    n = n + 1
    #Berechnung der Ratenfunktionen
    a1 = x[0] * c[0]
    a2 = 1 / 2 * x[0] * (x[0] - 1) * c[1]
    a3 = x[1] * c[2]
    a4 = x[1] * c[3]
    a = [a1, a2, a3, a4]
    a0 = sum(a)
    #Sample des Zeitschrittes
    tau = numpy.random.exponential(1 / a0)
    t = t + tau
    #Entscheidung welche Reaktion stattfindet
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
    #Speicherung des Zustands und Zeit
    time.append(t)
    S1.append(x[0])
    S2.append(x[1])
    S3.append(x[2])

#Anzahl der Schritte
print(n)

plt.plot(time, S1, ':')
plt.plot(time, S2,  ':')
plt.plot(time, S3, ':')
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.legend(('S1', 'S2', 'S3'))
plt.show()