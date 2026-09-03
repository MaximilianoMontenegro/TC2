#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 16:43:58 2026

@author: monezemax
"""

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Parámetros
# -------------------------------------------------

# Índice de muestras
n = np.arange(0, 30)

# Frecuencia digital de la senoide
omega_0 = 0.1 * np.pi

# -------------------------------------------------
# Señal de entrada
# -------------------------------------------------

x = np.sin(omega_0 * n)

# -------------------------------------------------
# Diferenciador propuesto
#
# y[n] = (x[n] - x[n-2]) / 2
# -------------------------------------------------

y = np.zeros_like(x)

for k in range(2, len(x)):
    y[k] = (x[k] - x[k-2]) / 2

# -------------------------------------------------
# Gráfico 1: entrada y salida del diferenciador
# -------------------------------------------------

plt.figure()

plt.stem(n, x,
         linefmt='C0-',
         markerfmt='C0o',
         basefmt=' ')

plt.stem(n, y,
         linefmt='C1-',
         markerfmt='C1s',
         basefmt=' ')

plt.xlabel('n [muestras]')
plt.ylabel('Amplitud')
plt.title('Entrada y salida del diferenciador')
plt.grid()
plt.legend(['x[n]', 'y[n]'])
plt.show()


# -------------------------------------------------
# Verificación utilizando np.diff()
# -------------------------------------------------

# np.diff calcula:
# x[n] - x[n-1]

y_diff = np.diff(x)

# np.diff genera una muestra menos
n_diff = n[1:]

# -------------------------------------------------
# Gráfico 2: comparación con np.diff
# -------------------------------------------------

plt.figure()

plt.stem(n, y,
         linefmt='C1-',
         markerfmt='C1s',
         basefmt=' ',
         label='Diferenciador')

plt.stem(n_diff, y_diff,
         linefmt='C2-',
         markerfmt='C2o',
         basefmt=' ',
         label='np.diff(x)')

plt.xlabel('n [muestras]')
plt.ylabel('Amplitud')
plt.title('Comparación del diferenciador con np.diff')
plt.grid()
plt.legend()
plt.show()


# -------------------------------------------------
# Derivada teórica de la senoide
#
# x[n] = sin(omega_0*n)
#
# dx/dn = omega_0*cos(omega_0*n)
# -------------------------------------------------

dx_teorica = omega_0 * np.cos(omega_0 * n)

# -------------------------------------------------
# Gráfico 3: comparación con la derivada teórica
# -------------------------------------------------

plt.figure()

plt.plot(n, dx_teorica,
         label='Derivada teórica')

plt.stem(n, y,
         linefmt='C1-',
         markerfmt='C1s',
         basefmt=' ',
         label='Diferenciador')

plt.stem(n_diff, y_diff,
         linefmt='C2-',
         markerfmt='C2o',
         basefmt=' ',
         label='np.diff(x)')

plt.xlabel('n [muestras]')
plt.ylabel('Amplitud')
plt.title('Comparación con la derivada teórica')
plt.grid()
plt.legend()
plt.show()