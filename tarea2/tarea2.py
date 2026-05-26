#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:16:09 2026

@author: monezemax
"""

import numpy as np
import scipy.signal as sig


# Ahora importamos las funciones de PyTC2

from pytc2.sistemas_lineales import analyze_sys, pretty_print_bicuad_omegayq, tf2sos_analog, pretty_print_SOS

from pytc2.general import print_subtitle

this_order = 5
this_ripple = 0.4


z,p,k = sig.buttap(this_order)

eps = np.sqrt( 10**(this_ripple/10) - 1 )
num, den = sig.zpk2tf(z,p,k)
num, den = sig.lp2lp(num, den, eps**(-1/this_order))

this_sos = tf2sos_analog(num, den)

pretty_print_SOS(this_sos, mode='omegayq')

num, den = sig.lp2hp(num, den)

this_sos = tf2sos_analog(num, den)

pretty_print_SOS(this_sos, mode='omegayq')

analyze_sys( this_sos )

den = np.array([1, 0, 640/256, 0, 560/256, 0, 200/256, 0 , 25/256, 0 , -1/256/ eps**2])
np.roots(den)
cheby_roots = np.roots(den)
cheby_roots = cheby_roots[ np.real(cheby_roots) < 0 ]
cheby_roots
p
num, den = sig.zpk2tf(z,p,k)
mi_tf = sig.TransferFunction(num,den)
from pytc2.sistemas_lineales import analyze_sys, pretty_print_bicuad_omegayq, tf2sos_analog, pretty_print_SOS
analyze_sys( mi_tf )
#%matplotlib auto
analyze_sys( mi_tf )
this_sos = tf2sos_analog(num, den)
pretty_print_SOS(this_sos, mode='omegayq')
from pytc2.sistemas_lineales import pretty_print_lti
pretty_print_lti(num,den)
cheby_roots
num 
den
pretty_print_SOS(this_sos, mode='omegayq')

print("\nRaíces Chebyshev:")
print(cheby_roots)

print("\nNumerador:")
print(num)

print("\nDenominador:")
print(den)