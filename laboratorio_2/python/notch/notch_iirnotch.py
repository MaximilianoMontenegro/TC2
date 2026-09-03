#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 00:25:48 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ==========================================
# FILTRO NOTCH CON iirnotch
# ==========================================

fs = 1000          # Frecuencia de muestreo [Hz]
f_notch = 50       # Frecuencia del notch [Hz]
BW = 1             # Ancho de banda a -3 dB [Hz]

# Factor de calidad
Q = f_notch / BW

# Diseño del filtro
b, a = signal.iirnotch(
    w0=f_notch,
    Q=Q,
    fs=fs
)

# Mostrar resultados
print("Q =", Q)

print("\nCoeficientes b:")
print(b)

print("\nCoeficientes a:")
print(a)

print("\nOrden:")
print(len(a) - 1)

# ==========================================
# RESPUESTA EN FRECUENCIA + PLANTILLA
# ==========================================

f, H = signal.freqz(b, a, worN=65536, fs=fs)

H_dB = 20 * np.log10(
    np.maximum(np.abs(H), 1e-12)
)

# Límites del ancho de banda
f1 = f_notch - BW/2
f2 = f_notch + BW/2

plt.figure(figsize=(9, 5))

# Respuesta del filtro
plt.plot(
    f,
    H_dB,
    linewidth=2,
    label="Filtro Notch"
)

# ==========================================
# PLANTILLA - ZONA NO PERMITIDA
# ==========================================

plt.fill_between(
    f,
    -3,
    5,
    where=((f >= f1) & (f <= f2)),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0,
    label='Zona no permitida'
)

# Frecuencia central
plt.axvline(
    f_notch,
    linestyle='--',
    label='f_notch = 50 Hz'
)

# Límites del BW
plt.axvline(
    f1,
    linestyle='--',
    label='f1 = 49.5 Hz'
)

plt.axvline(
    f2,
    linestyle='--',
    label='f2 = 50.5 Hz'
)

# Nivel de -3 dB
plt.axhline(
    -3,
    linestyle='--',
    label='-3 dB'
)

# ==========================================

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Filtro Notch - Respuesta y plantilla')

plt.xlim(45, 55)
plt.ylim(-60, 5)

plt.grid()
plt.legend()

plt.show()

# ==========================================
# POLOS Y CEROS
# ==========================================

z, p, k = signal.tf2zpk(b, a)

print("\nCeros:")
print(z)

print("\nPolos:")
print(p)

print("\nMódulo de los polos:")
print(np.abs(p))

# Circunferencia unitaria
theta = np.linspace(0, 2*np.pi, 500)

plt.figure(figsize=(6, 6))

plt.plot(
    np.cos(theta),
    np.sin(theta),
    '--',
    label='Circunferencia unitaria'
)

# Ceros
plt.scatter(
    np.real(z),
    np.imag(z),
    marker='o',
    facecolors='none',
    s=100,
    label='Ceros'
)

# Polos
plt.scatter(
    np.real(p),
    np.imag(p),
    marker='x',
    s=100,
    label='Polos'
)

plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)

plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginaria')
plt.title('Diagrama de Polos y Ceros - Notch')

plt.grid()
plt.axis('equal')
plt.legend()

plt.show()  