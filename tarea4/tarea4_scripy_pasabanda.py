#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 22:19:38 2026

@author: monezemax
"""
# Módulos externos

import sympy as sp
from sympy.abc import s

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
import scipy.signal as sig
from IPython.display import display, Markdown

# Ahora importamos las funciones de PyTC2

from pytc2.sistemas_lineales import analyze_sys, parametrize_sos, pretty_print_lti, pretty_print_bicuad_omegayq, tf2sos_analog, pretty_print_SOS
from pytc2.general import print_latex, print_subtitle, a_equal_b_latex_s

fig_sz_x = 13
fig_sz_y = 7
fig_dpi = 80 # dpi

fig_font_size = 11

mpl.rcParams['figure.figsize'] = (fig_sz_x, fig_sz_y)
mpl.rcParams['figure.dpi'] = fig_dpi
plt.rcParams.update({'font.size':fig_font_size})

# se define el pasabajo
num = np.array([0.7157])
den = np.array([1 , 1.253 , 1.535 , 0.7157])

# Q de la transformación
Q = 5

#obtengo el pasabanda
num_pb , den_pb = sig.lp2bp(num, den, bw=1/Q)

print_subtitle('Filtro pasabajos obtenido')

print_latex(a_equal_b_latex_s('$ T_{lp}(s)', pretty_print_lti(num, den, displaystr=False)))

print_subtitle('Pasabanda obtenido para Q={:d} (coeficientes de los polinomios)'.format(Q))

print_subtitle('Como cociente de polinomios')

# forma un poco más clara
print_latex(a_equal_b_latex_s('T_{bp}(s)', pretty_print_lti(num_pb, den_pb, displaystr=False)))

T1_bp =  sig.TransferFunction( num_pb, den_pb )

# el caracter "_" descarta la salida de la función
_= analyze_sys([T1_bp], sys_name='Filtro pasabanda totalQ={:d}'.format(Q))

print_subtitle('Pasabanda factorizado en secciones bicuadráticas (SOS)')

sos_pbanda = tf2sos_analog(num_pb, den_pb)

# la visualizamos de algunas formas, la tradicional
#pretty_print_SOS(sos_pbanda)
print_latex(a_equal_b_latex_s('T_{bp}(s)', pretty_print_SOS(sos_pbanda, displaystr=False)))

# ====================================
# Graficar cada SOS por separado
# ====================================

sos_systems = []
sos_names = []

for ii, this_sos in enumerate(sos_pbanda):

    num_sos = this_sos[:3]
    den_sos = this_sos[3:]

    sos_systems.append(
        sig.TransferFunction(num_sos, den_sos)
    )
    
for ii, this_sos in enumerate(sos_pbanda):

    print_subtitle(f'SOS {ii+1}')

    pretty_print_lti(
        this_sos[:3],
        this_sos[3:]
    )

    sos_names.append(f'SOS {ii+1}')

# Graficar únicamente las SOS
_ = analyze_sys(sos_systems, sos_names)

all_sys = [T1_bp] + sos_systems

all_names = ['Filtro total'] + sos_names

_ = analyze_sys(all_sys, all_names)
