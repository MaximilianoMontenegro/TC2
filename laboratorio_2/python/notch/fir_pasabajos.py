#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:36:55 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ==========================================
# FIR PASA-BAJOS
# ==========================================

fs = 40000      # Frecuencia de muestreo [Hz]

fp = 100        # Fin de banda de paso [Hz]
fst = 300       # Inicio de banda de rechazo [Hz]

# Especificaciones de amplitud
gpass = 1       # Atenuación máxima en banda de paso [dB]
gstop = 60      # Atenuación mínima en banda de rechazo [dB]

# Ancho de banda de transición
BW = fst - fp

print("Banda de transición =", BW, "Hz")

# Frecuencia central de la transición
fc = (fp + fst) / 2

# Cantidad de taps
num_taps = 93

# Diseño FIR con ventana Hamming
fir_taps = signal.firwin(
    numtaps=num_taps,
    cutoff=fc,
    window='hamming',
    fs=fs
)

print("\nFrecuencia de diseño =", fc, "Hz")
print("Cantidad de taps =", len(fir_taps))

# ==========================================
# RESPUESTA EN FRECUENCIA
# ==========================================

f, H = signal.freqz(
    fir_taps,
    worN=65536,
    fs=fs
)

H_dB = 20 * np.log10(
    np.maximum(np.abs(H), 1e-12)
)

plt.figure(figsize=(9, 5))

# Respuesta del filtro
plt.plot(
    f,
    H_dB,
    linewidth=2,
    label='FIR pasa-bajos'
)

# ==========================================
# PLANTILLA - ZONAS NO PERMITIDAS
# ==========================================

# Banda de paso:
# la respuesta NO debe caer por debajo de -gpass
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

# Banda de rechazo:
# la respuesta NO debe estar por encima de -gstop
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

# ==========================================
# LÍMITES DE LA PLANTILLA
# ==========================================

plt.axvline(
    fp,
    linestyle='--',
    label='fp = 100 Hz'
)

plt.axvline(
    fst,
    linestyle='--',
    label='fs = 300 Hz'
)

plt.axhline(
    -gpass,
    linestyle='--',
    label='gpass = 1 dB'
)

plt.axhline(
    -gstop,
    linestyle='--',
    label='gstop = 60 dB'
)

# ==========================================

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Filtro FIR pasa-bajos - Respuesta y plantilla')

plt.xlim(0, 600)
plt.ylim(-100, 5)

plt.grid()
plt.legend()

plt.show()

# ==========================================
# ATENUACIÓN A 300 Hz
# ==========================================
    
f_medicion = 300

# Buscar el punto de la respuesta más cercano a 300 Hz
idx = np.argmin(np.abs(f - f_medicion))

atenuacion_300 = H_dB[idx]

print("\n================================")
print("Respuesta a 300 Hz")
print("================================")
print(f"Frecuencia = {f[idx]:.2f} Hz")
print(f"Ganancia    = {atenuacion_300:.2f} dB")
print(f"Atenuación  = {-atenuacion_300:.2f} dB")

print("\nCoeficientes FIR para STM32:\n")

for coef in fir_taps[::-1]:
    print(f"{coef:.10e}f,")