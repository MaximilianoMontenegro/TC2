#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:10:39 2026

@author: monezemax
"""

import sympy as sp

from pytc2.dibujar import dibujar_Pi, dibujar_Tee
from pytc2.cuadripolos import calc_MAI_impedance_ij, calc_MAI_vtransf_ij_mn, calc_MAI_ztransf_ij_mn
from pytc2.cuadripolos import Y2Tabcd_s
from pytc2.general import print_latex, print_subtitle, a_equal_b_latex_s
from IPython.display import display, Latex, Markdown
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def print_latex(unstr):
    display(Latex(r'$$' + unstr + r'$$'))


# T puenteado cargado: red de R constante
# explicación:
'''    
+ Numeramos los polos de 0 a n=3

1 ---- sL ----o---- sL ---- 2
             |
            1/(sC)
             |
             3
'''    

## dibijo el circuito:
import schemdraw
import schemdraw.elements as elm

print("ciruito tee")

with schemdraw.Drawing() as d:

    # Nodo 1
    d += elm.Dot(open=True).label('1')
    
    # Inductor Za = sL
    d += elm.Inductor().right().label(r'$L$')

    # Nodo central
    nodo = d.here
    d += elm.Dot()

    # Inductor Zc = sL
    d += elm.Inductor().right().label(r'$L$')

    # Nodo 2
    d += elm.Dot(open=True).label('2')

    # Volvemos al nodo central
    d.push()
    d.move_from(nodo)

    # Capacitor hacia nodo 3
    d += elm.Capacitor().down().label(r'$C$')
    d += elm.Dot(open=True).label('3')

    d.pop()
    

print("Mosfet")
with schemdraw.Drawing() as d:

    # Nodo Gate
    g = d.here
    d += elm.Dot(open=True).label('G')

    # Rama superior: Cgd hacia Drain
    d += elm.Capacitor().right().label(r'$C_{gd}$')
    d_node = d.here
    d += elm.Dot(open=True).label('D')

    # Volvemos a Gate para dibujar Cgs hacia Source
    d.move_from(g)
    d += elm.Capacitor().down().label(r'$C_{gs}$')
    s_node = d.here
    d += elm.Dot(open=True).label('S')

    # Cds entre Drain y Source
    d.move_from(d_node)
    d += elm.Capacitor().down().label(r'$C_{ds}$')
    d += elm.Line().left().tox(s_node)

    # Fuente de corriente controlada gm*Vgs
    d.move_from(d_node)
    d += elm.Line().right().length(1.5)

    fuente = elm.SourceControlledI().down()
    d += fuente

    # Etiqueta a la derecha de la fuente
    d += elm.Label().at(
        (fuente.center[0] + 0.7, fuente.center[1])
    ).label(r'$g_m V_{gs}$')

    d += elm.Line().left().tox(s_node)

# declaro los simbolos para ambas matrices
s, L, C = sp.symbols('s L C')
s, Cgs, Cgd, Cds, gm = sp.symbols('s C_gs C_gd C_ds g_m')

## Armo la matriz de admitancia indeterminada #####################
Ymai = sp.Matrix([
    [
        (s**2*L*C + 1)/(s*L*(s**2*L*C + 2)),
        -1/(s*L*(s**2*L*C + 2)),
        -s*C/(s**2*L*C + 2)
    ],
    [
        -1/(s*L*(s**2*L*C + 2)),
        (s**2*L*C + 1)/(s*L*(s**2*L*C + 2)),
        -s*C/(s**2*L*C + 2)
    ],
    [
        -s*C/(s**2*L*C + 2),
        -s*C/(s**2*L*C + 2),
        2*s*C/(s**2*L*C + 2)
    ]
])


Ymos = sp.Matrix([
    [
        s*(Cgs + Cgd),
        -s*Cgd,
        -s*Cgs
    ],
    [
        gm - s*Cgd,
        s*(Cgd + Cds),
        -gm - s*Cds
    ],
    [
        -gm - s*Cgs,
        -s*Cds,
        gm + s*(Cgs + Cds)
    ]
])
######################################################################


con_detalles = False

print_subtitle('Matriz Admitancia Indefinida:')
print_latex(a_equal_b_latex_s('Y_MAI', Ymai))

print_subtitle('Matriz Admitancia Indefinida del MOSFET:')
print_latex(a_equal_b_latex_s('Y_{MAI}', Ymos))


print("Obtengo las transferencias:")

V2313 = calc_MAI_vtransf_ij_mn(
    Ymai,
    1, 2,   # V23
    0, 2,   # V13
    verbose=con_detalles
)

V2131 = calc_MAI_vtransf_ij_mn(
    Ymai,
    1, 0,   # 2,1
    2, 0,   # 3,1
    verbose=con_detalles
)
V1232 = calc_MAI_vtransf_ij_mn(
    Ymai,
    0, 1,   # V12
    2, 1,   # V32
    verbose=con_detalles
)

V2313 = sp.simplify(V2313)
V2131 = sp.simplify(V2131)
V1232 = sp.simplify(V1232)


print_latex(
    r'\frac{V_{23}}{V_{13}} = ' + sp.latex(V2313)
)
print_latex(
    r'\frac{V_{21}}{V_{31}} = ' + sp.latex(V2131)
)
print_latex(
    r'\frac{V_{12}}{V_{32}} = ' + sp.latex(V1232)
)


#### grafico modulo y fase  ############################
print_subtitle('Modulo y fase de las transferencias')

# ============================================================
# Valores numéricos de L y C
# ============================================================

L_val = 1      # [H]
C_val = 1      # [F]

valores = {
    L: L_val,
    C: C_val
}


# ============================================================
# Función para graficar módulo y fase
# ============================================================

def graficar_bode(H, titulo):

    # Reemplazo L y C por valores numéricos
    H_num = sp.simplify(H.subs(valores))

    # Convierto la expresión simbólica a una función numérica
    H_fun = sp.lambdify(s, H_num, 'numpy')

    # Vector de frecuencia [Hz]
    f = np.logspace(-2, 2, 10000)

    # Frecuencia angular
    w = 2*np.pi*f

    # Evaluación en s = jw
    H_jw = H_fun(1j*w)

    # Módulo en dB
    modulo = 20*np.log10(np.abs(H_jw))

    # Fase en grados
    fase = np.unwrap(np.angle(H_jw)) * 180/np.pi

    # ----------------------------
    # Gráfico de módulo
    # ----------------------------
    plt.figure()
    plt.semilogx(f, modulo)
    plt.grid(True, which='both')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Módulo [dB]')
    plt.title(titulo + ' - Módulo')
    plt.show()

    # ----------------------------
    # Gráfico de fase
    # ----------------------------
    plt.figure()
    plt.semilogx(f, fase)
    plt.grid(True, which='both')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Fase [°]')
    plt.title(titulo + ' - Fase')
    plt.show()


# ============================================================
# Grafico las tres transferencias
# ============================================================

graficar_bode(
    V2313,
    r'$V_{23}/V_{13}$'
)

graficar_bode(
    V2131,
    r'$V_{21}/V_{31}$'
)

graficar_bode(
    V1232,
    r'$V_{12}/V_{32}$'
)

###############################################################
#### Matriz admitancia en source comun ########################

print("matriz admitancia del mosfet en surce común")
Y_SC = sp.Matrix([
    [s*(Cgs + Cgd),      -s*Cgd],
    [gm - s*Cgd,     s*(Cgd + Cds)]
])

print_subtitle('Matriz Admitancia definida del MOSFET:')
print_latex(a_equal_b_latex_s('Y_{MAD}', Y_SC))

T_SC = Y2Tabcd_s(Y_SC)

print_subtitle('Matriz ABCD - Source común:')
print_latex(
    a_equal_b_latex_s('T_{ABCD}', sp.simplify(T_SC))
)