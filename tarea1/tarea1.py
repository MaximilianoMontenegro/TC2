#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 19:45:45 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# ============================================================
# Transferencia en Laplace
# Ejemplo:
#             
# H(s) = -----------
#        s^2 + s + 1
# ============================================================

R = 6772.5
R1 = 6954.54
R3 = R1
R4 = 9e3
R5 = 1e3
C = 47e-9
C1 = 1e-9

Q = 1/(R*C)

w02 = R4/(R1*R3*R5*C*C1)

Av_0hz = (R4 + R5)/(R*R5*C)

num = [Av_0hz,0]
den = [1, Q, w02]

sistema = signal.TransferFunction(num, den)

# ============================================================
# Respuesta en frecuencia: s = jw
# ============================================================

f = np.logspace(2, 6, 1000)  # rad/s

w = 2*np.pi*f

w, mag, phase = signal.bode(sistema, w)

plt.figure()
plt.semilogx(f, mag)
plt.grid(True, which="both")
plt.xlabel("Frecuencia f [Hz]")
plt.ylabel("Magnitud [dB]")
plt.title("Respuesta en frecuencia - Magnitud")

# Frecuencia central aproximada
f0 = np.sqrt(w02)/(2*np.pi)

# Barrido lineal alrededor de f0
f_lineal = np.linspace(f0/5, f0*5, 2000)

w_lineal = 2*np.pi*f_lineal

w_lineal, mag_lineal, phase_lineal = signal.bode(sistema, w_lineal)

plt.figure()
plt.plot(f_lineal, mag_lineal)
plt.grid(True)
plt.xlabel("Frecuencia f [Hz]")
plt.ylabel("Magnitud [dB]")
plt.title("Respuesta en frecuencia lineal - Magnitud")
plt.show()

plt.figure()
plt.semilogx(f, phase)
plt.grid(True, which="both")
plt.xlabel("Frecuencia f [Hz/s]")
plt.ylabel("Fase [°]")
plt.title("Respuesta en frecuencia - Fase")

# ============================================================
# Diagrama de polos y ceros
# ============================================================

ceros, polos, ganancia = signal.tf2zpk(num, den)

plt.figure()

plt.plot(np.real(ceros), np.imag(ceros), "o", markersize=10,
         fillstyle="none", label="Ceros")

plt.plot(np.real(polos), np.imag(polos), "x", markersize=10,
         label="Polos")

plt.axhline(0)
plt.axvline(0)

plt.grid(True)
plt.xlabel("Parte real σ")
plt.ylabel("Parte imaginaria jω")
plt.title("Diagrama de polos y ceros en el plano s")
plt.legend()

plt.show()

print("Ceros:", ceros)
print("Polos:", polos)
print("Ganancia:", ganancia)