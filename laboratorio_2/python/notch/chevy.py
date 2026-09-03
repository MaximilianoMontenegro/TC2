#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 00:04:33 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ==========================================
# FILTRO A - CHEBYSHEV
# ==========================================

# Frecuencia de muestreo
fs = 1000  # Hz

# Especificaciones
fp = 100   # Frecuencia de banda de paso [Hz]
fst = 300  # Frecuencia de banda de rechazo [Hz]

gpass = 1   # Atenuación máxima en banda de paso [dB]
gstop = 60  # Atenuación mínima en banda de rechazo [dB]

# Diseño del filtro
b, a = signal.iirdesign(
    wp=fp,
    ws=fst,
    gpass=gpass,
    gstop=gstop,
    ftype='cheby1',
    fs=fs,
    output='ba'
)

print("Coeficientes b:")
print(b)

print("\nCoeficientes a:")
print(a)

print("\nOrden del filtro:")
print(len(a) - 1)

## ==========================================
# RESPUESTA EN FRECUENCIA + PLANTILLA
# ==========================================

f, H = signal.freqz(b, a, worN=8192, fs=fs)

H_dB = 20 * np.log10(np.abs(H))

plt.figure(figsize=(9, 5))

# Respuesta del filtro
plt.plot(f, H_dB, linewidth=2, label="Chebyshev")

# ==========================================
# ZONAS PROHIBIDAS DE LA PLANTILLA
# ==========================================

# Banda de paso - zona no permitida
plt.fill_between(
    f,
    -100,
    -gpass,
    where=(f <= fp),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0,
    label='Zona no permitida'
)

# Banda de rechazo - zona no permitida
plt.fill_between(
    f,
    -gstop,
    5,
    where=(f >= fst),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0
)

# Límites de la plantilla
plt.axvline(fp, linestyle="--", label="fp = 100 Hz")
plt.axvline(fst, linestyle="--", label="fs = 300 Hz")

plt.axhline(-gpass, linestyle="--", label="αmax = 1 dB")
plt.axhline(-gstop, linestyle="--", label="αmin = 60 dB")

# ==========================================

plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud [dB]")
plt.title("Filtro Chebyshev - Plantilla de diseño")

plt.xlim(0, fs/2)
plt.ylim(-100, 5)

plt.grid()
plt.legend()
plt.show()

# ==========================================
# DIAGRAMA DE POLOS Y CEROS
# ==========================================

# Obtener ceros, polos y ganancia
z, p, k = signal.tf2zpk(b, a)

# Circunferencia unitaria
theta = np.linspace(0, 2*np.pi, 500)

plt.figure(figsize=(6, 6))

plt.plot(np.cos(theta), np.sin(theta), '--', label='Circunferencia unitaria')

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

# Ejes
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)

plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginaria')
plt.title('Diagrama de Polos y Ceros')

plt.grid()
plt.axis('equal')
plt.legend()

plt.show()

print("\nCeros:")
print(z)

print("\nPolos:")
print(p)

print("\nMódulo de los polos:")
print(np.abs(p))