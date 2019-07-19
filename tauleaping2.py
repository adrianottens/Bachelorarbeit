import math
import numpy
import matplotlib.pyplot as plt
c1 = 0.001
c2 = 0.1
epsilon = [0.01, 0.03, 0.05, 0.1, 0.15, 0.2]
nc = 5
Error = []
DL = []
for eps in epsilon:
    k = 0
    Leaps = []
    negativeError = 0
    while k != 10**4:
        x = [499, 1, 0]
        t = 0.0
        n = 0
        ssa = 0
        '''State = [(S, i, R)]
        time = [t]'''
        while x[1] != 0 or x[2] != 500:
            a1 = x[0]*x[1]*c1
            a2 = x[1]*c2
            a0 = a1 + a2
            a = [a1, a2]
            if a0 == 0:
                break
            f = [[-x[1]*c1+x[0]*c1, -x[0]*c1], [c2, -c2]]
            u = [0, 0]
            o = [0, 0]
            for i in [0, 1]:
                for j in [0, 1]:
                    u[i] = u[i] + f[i][j] * a[j]
                    o[i] = o[i] + ((f[i][j])**2) * a[j]
            if u[0] == 0 or u[1] == 0:
                tau = numpy.random.exponential(1/a0)
            else:
                tau = min((eps*a0)/abs(u[0]), (eps*a0)/abs(u[1]), (eps * a0) ** 2 / o[0], (eps * a0) ** 2 / o[0])
            if tau < 5/a0:
                m = 0
                while m != 100:
                    a1 = x[0] * x[1] * c1
                    a2 = x[1] * c2
                    a0 = a1 + a2
                    if a0 == 0:
                        break
                    tau = numpy.random.exponential(1 / a0)
                    temp = numpy.random.uniform(0.0, 1.0)
                    if temp < a1/a0:
                        x[0] = x[0] - 1
                        x[1] = x[1] + 1
                    else:
                        x[1] = x[1] - 1
                        x[2] = x[2] + 1
                    n = n + 1
                    if x[1] == 0 or x[2] == 500:
                        break
                    m = m + 1
                ssa = ssa + m
            else:
                sample = [0, 0]
                sample[0] = numpy.random.poisson(a[0]*tau)
                sample[1] = numpy.random.poisson(a[1]*tau)
                x[0] = x[0] - sample[0]
                x[1] = x[1] + sample[0] - sample[1]
                x[2] = x[2] + sample[1]
                n = n + 1
            if x[0] < 0 or x[1] < 0:
                negativeError = negativeError + 1
                break
        Leaps.append(n)
        k = k + 1
    DL.append(sum(Leaps)/10**4)
    Error.append(negativeError)
    print(eps)
print(Error)
print(DL)
