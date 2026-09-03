#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 23:52:50 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ==========================================
# FILTRO B - NOTCH CON IIRDESIGN
# ==========================================

fs = 1000  # Hz

# Bordes
wp = [49, 51]
ws = [49.5, 50.5]

# Atenuaciones
gpass = 1
gstop = 40

# Diseño
b, a = signal.iirdesign(
    wp=wp,
    ws=ws,
    gpass=gpass,
    gstop=gstop,
    ftype='ellip',
    fs=fs,
    output='ba'
)

print("Coeficientes b:")
print(b)

print("\nCoeficientes a:")
print(a)

print("\nOrden:")
print(len(a) - 1)

# ==========================================
# RESPUESTA EN FRECUENCIA + PLANTILLA
# NOTCH CON iirdesign
# ==========================================

f, H = signal.freqz(b, a, worN=65536, fs=fs)

H_dB = 20 * np.log10(
    np.maximum(np.abs(H), 1e-12)
)

# Bordes usados en el diseño
fp1 = 49
fs1 = 49.5
fs2 = 50.5
fp2 = 51

plt.figure(figsize=(9, 5))

# Respuesta del filtro
plt.plot(
    f,
    H_dB,
    linewidth=2,
    label='Notch - iirdesign'
)

# ==========================================
# PLANTILLA
# ==========================================

# Zona no permitida en banda de paso izquierda
plt.fill_between(
    f,
    -100,
    -gpass,
    where=(f <= fp1),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0,
    label='Zona no permitida'
)

# Zona no permitida en banda de rechazo
plt.fill_between(
    f,
    -gstop,
    5,
    where=((f >= fs1) & (f <= fs2)),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0
)

# Zona no permitida en banda de paso derecha
plt.fill_between(
    f,
    -100,
    -gpass,
    where=(f >= fp2),
    facecolor='none',
    edgecolor='red',
    hatch='//',
    linewidth=0.0
)

# ==========================================
# Límites de frecuencia
# ==========================================

plt.axvline(
    fp1,
    linestyle='--',
    label='fp1 = 49 Hz'
)

plt.axvline(
    fs1,
    linestyle='--',
    label='fs1 = 49.5 Hz'
)

plt.axvline(
    fs2,
    linestyle='--',
    label='fs2 = 50.5 Hz'
)

plt.axvline(
    fp2,
    linestyle='--',
    label='fp2 = 51 Hz'
)

# Límites de atenuación
plt.axhline(
    -gpass,
    linestyle='--',
    label='gpass = 1 dB'
)

plt.axhline(
    -gstop,
    linestyle='--',
    label='gstop = 40 dB'
)

# Frecuencia central
plt.axvline(
    50,
    linestyle=':',
    label='f0 = 50 Hz'
)

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Filtro Notch - iirdesign con plantilla')

plt.xlim(45, 55)
plt.ylim(-100, 5)

plt.grid()
plt.legend()

plt.show()

# ==========================================
# DIAGRAMA DE POLOS Y CEROS
# ==========================================

# Obtener ceros, polos y ganancia
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

# Circunferencia unitaria
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

# Ejes
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)

plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginaria')
plt.title('Diagrama de Polos y Ceros - Notch iirdesign')

plt.grid()
plt.axis('equal')
plt.legend()

plt.show()