import numpy
import matplotlib.pyplot as plt
#Anfangszustand
x = [25, 25, 0]
StateX1 = [x[0]]
StateX3 = [x[2]]

#Reaktionskonstanten
c1 = 1
c2 = 2

#Zeit
t = 0.0
Time = [t]

#Endzeit
Tend = 1

n = 0
while t < Tend:
    #Berechnung der Ratenfunktionen
    a1 = x[2]*c1
    a2 = x[1]*x[0]*c2
    a0 = a1 + a2
    #Sample von tau
    tau = numpy.random.exponential(1/a0)
    t = t + tau
    Time.append(t)
    temp = numpy.random.uniform(0.0, 1.0, 1)
    #Samplen welche Reaktion stattfindet
    if temp<a1/a0:
        x[2] = x[2] - 1
        x[0] = x[0] + 1
        x[1] = x[1] + 1
    else:
        x[2] = x[2] + 1
        x[0] = x[0] - 1
        x[1] = x[1] - 1
    StateX1.append(x[0])
    StateX3.append(x[2])
    n = n + 1
#Anzahl an Schritte
print(n)

plt.step(Time, StateX1, ':')
plt.step(Time, StateX3, ':')
plt.xlabel('Zeit')
plt.ylabel('Population')
plt.title('reversibles Binden-Losbinden')
plt.legend(('S_1','S_3'))
plt.show()
