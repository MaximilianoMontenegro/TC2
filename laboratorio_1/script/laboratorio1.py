#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 11:29:06 2026

@author: monezemax
"""

# Inicialización e importación de módulos

# Módulos externos
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

from pytc2.sistemas_lineales import analyze_sys, pretty_print_bicuad_omegayq, tf2sos_analog, pretty_print_SOS, pretty_print_lti

from pytc2.general import print_subtitle

fig_sz_x = 13
fig_sz_y = 7
fig_dpi = 80 # dpi

fig_font_size = 11

this_order = 2

mpl.rcParams['figure.figsize'] = (fig_sz_x, fig_sz_y)
mpl.rcParams['figure.dpi'] = fig_dpi
plt.rcParams.update({'font.size':fig_font_size})

def sim_aprox(aproxs, orders2analyze, ripple, attenuation):

    all_sys = []
    filter_names = []

    for (this_aprox, this_order, this_ripple, this_att) in zip(aproxs, orders2analyze, ripple, attenuation):

        if this_aprox == 'Butterworth':

            z,p,k = sig.buttap(this_order)

            eps = np.sqrt( 10**(this_ripple/10) - 1 )
            num, den = sig.zpk2tf(z,p,k)
            num, den = sig.lp2lp(num, den, eps**(-1/this_order))

            z,p,k = sig.tf2zpk(num, den)

        elif this_aprox == 'Chebyshev1':

            z,p,k = sig.cheb1ap(this_order, this_ripple)

        elif this_aprox == 'Chebyshev2':

            z,p,k = sig.cheb2ap(this_order, this_att)

        elif this_aprox == 'Bessel':

            z, p, k = sig.besselap(this_order, norm='delay')

            num, den = sig.zpk2tf(z, p, k)

            tau = 100e-6
            fw = 5000

            Omega_w = 2*np.pi*fw
            Omega_s = (1/tau) / Omega_w

            num, den = sig.lp2lp(num, den, Omega_s)

            z, p, k = sig.tf2zpk(num, den)
        elif this_aprox == 'Cauer':

            z,p,k = sig.ellipap(this_order, this_ripple, this_att)


        num, den = sig.zpk2tf(z,p,k)

        
        all_sys.append(sig.TransferFunction(num,den))

        #this_label = this_aprox + '_ord_' + str(this_order) + '_rip_' + str(this_ripple)+ '_att_' + str(this_att)
        this_label = this_aprox + '_ord_' + str(this_order)
        print_subtitle(this_label)
        # factorizamos en SOS's
        try:
            this_sos = tf2sos_analog(num, den)
        except ValueError:
            this_sos = sig.tf2sos(num, den, pairing='nearest')
        
        pretty_print_lti(num,den)
        pretty_print_SOS(this_sos, mode='omegayq')        
        
        
        filter_names.append(this_label)
        
    # el caracter "_" descarta la salida de la función
    _ = analyze_sys( all_sys, filter_names )

    return( all_sys, filter_names )

#aprox_name = 'Butterworth'
#aprox_name = 'Chebyshev1'
#aprox_name = 'Chebyshev2'
aprox_name = 'Bessel'
#aprox_name = 'Cauer'

# parametrizamos el orden para cada aproximación
#orders2analyze = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
orders2analyze = [2,3,4,5]
alpha_max = [1]

# Mismo requerimiento de ripple y atenuación
aproxs = [aprox_name] * len(orders2analyze)
ripple = alpha_max * len(orders2analyze) # dB \alpha_{max} <-- Sin parametrizar, lo dejo en Butterworth
attenuation = [1] * len(orders2analyze) # dB \alpha_{min} <-- Sin parametrizar, att fija


print_subtitle('Aproximaciones de Bessel')

( all_sys, filter_names ) = sim_aprox(aproxs, orders2analyze, ripple, attenuation)

for H, nombre in zip(all_sys, filter_names):

    w = np.logspace(-2, 2, 2000)

    w, h = sig.freqs(H.num, H.den, w)

    fase = np.unwrap(np.angle(h))
    tau_g = -np.gradient(fase, w)

    # Frecuencias normalizadas
    Omega_3k = 3000/5000
    Omega_5k = 1

    idx = np.argmin(np.abs(w - Omega_3k))

    tau_3k = tau_g[idx]

    tau = 100e-6
    fw = 5000
    Omega_w = 2*np.pi*fw
    Omega_s = (1/tau) / Omega_w

    tau_0 = 1/Omega_s

    desvio = abs(tau_3k - tau_0)/tau_0 * 100

    _, h5 = sig.freqs(H.num, H.den, [Omega_5k])

    att_5k = -20*np.log10(abs(h5[0]))

    print("\n" + "="*50)
    print(nombre)
    print(f"τg_norm(3 kHz) = {tau_3k:.4f}")
    print(f"Desvío         = {desvio:.2f} %")
    print(f"Att(5 kHz)     = {att_5k:.2f} dB")

    if desvio <= 2 and att_5k <= 1:
        print(">>> CUMPLE <<<")