import numpy as np
import matplotlib.pyplot as plt
import math

data1 = np.loadtxt('LotSSAbinsX1.dat')
data2 = np.loadtxt('LotSSAbinsX2.dat')
data3 = np.loadtxt('LotSSAbinsX3.dat')
data4 = np.loadtxt('LotSSANX1.dat')
data5 = np.loadtxt('LotSSANX2.dat')
data6 = np.loadtxt('LotSSANX3.dat')
data7 = np.loadtxt('LotkaRX101.dat')
data8 = np.loadtxt('LotkaRX201.dat')
data9 = np.loadtxt('LotkaRX301.dat')
data10 = np.loadtxt('LotkaRX103.dat')
data11 = np.loadtxt('LotkaRX203.dat')
data12 = np.loadtxt('LotkaRX303.dat')
data13 = np.loadtxt('LotkaRX105.dat')
data14 = np.loadtxt('LotkaRX205.dat')
data15 = np.loadtxt('LotkaRX305.dat')
data16 = np.loadtxt('LotkaRX11.dat')
data17 = np.loadtxt('LotkaRX21.dat')
data18 = np.loadtxt('LotkaRX31.dat')

Error01 = 0
Error03 = 0
Error05 = 0
Error1 = 0

delta1 = []
delta2 = []
delta3 = []

for j in range(0, 25):
    delta1.append(data1[j, :][1] - data1[j, :][0])
    delta2.append(data2[j, :][1] - data2[j, :][0])
    delta3.append(data3[j, :][1] - data3[j, :][0])

for i in range(0, 25):
    Error01 = Error01 + delta1[i] * sum(abs(data4[i, :] - data7[i, :])) + delta2[i] * sum(
        abs(data5[i, :] - data8[i, :])) \
              + delta3[i] * sum(abs(data6[i, :] - data9[i, :]))
    Error03 = Error03 + delta1[i] * sum(abs(data4[i, :] - data10[i, :])) + delta2[i] * sum(
        abs(data5[i, :] - data11[i, :])) \
              + delta3[i] * sum(abs(data6[i, :] - data12[i, :]))
    Error05 = Error05 + delta1[i] * sum(abs(data4[i, :] - data13[i, :])) + delta2[i] * sum(
        abs(data5[i, :] - data14[i, :])) \
              + delta3[i] * sum(abs(data6[i, :] - data15[i, :]))
    Error1 = Error1 + delta1[i] * sum(abs(data4[i, :] - data16[i, :])) + delta2[i] * sum(
        abs(data5[i, :] - data17[i, :])) \
             + delta3[i] * sum(abs(data6[i, :] - data18[i, :]))
Error01 = Error01 / 75
Error03 = Error03 / 75
Error05 = Error05 / 75
Error1 = Error1 / 75
np.savetxt('LotkaRError.dat', [Error01, Error03, Error05, Error1])
m = np.loadtxt('LotkaTauError.dat')
K = math.sqrt(40 / (math.pi * 10 ** 4))
plt.plot([0.01, 0.03, 0.05, 0.1], [K, K, K, K])
plt.plot([0.01, 0.03, 0.05, 0.1], [Error01, Error03, Error05, Error1], marker='v')
plt.plot([0.01, 0.03, 0.05, 0.1], m, marker='o')
plt.show()


