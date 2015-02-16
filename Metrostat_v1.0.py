# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 16:05:44 2015

@author: Wimma
"""

from __future__ import division
from numpy import linspace
from scipy.integrate import odeint
from matplotlib import pyplot as plot

"Declare the constants and initial conditions"

# constants
k1 = 1.842192
k2 = 26.639385
k3 = 2.828542
k4 = 0.953015
k5 = 0.009999
k6 = 26.821861
k7 = 0.638429
k8 = 1.934807
k9 = 4.255633
k10 = 5.969177
k11 = 2.784037
k12 = 1.000000
Area = 1.000000

# initial conditions
HCl_0 = 0
LDH_0 = 0.3
Poly_active_0 = 5
Radical_0 = 0
Prim_stab_0 = 1.3
Poly_deg_0 = 0
Cross_link_0 = 0

# save in a single list
initial = [HCl_0, LDH_0, Poly_active_0, Radical_0, Prim_stab_0,
           Poly_deg_0, Cross_link_0]

"Set up differential model"


def metrostat(Variables, Time):

    """
    Name convention:
    HCl             Concentration of HCl gas in PVC
    LDH             Concentration of secondary stabiliser (LDH) in PVC
    Poly_active     Concentration of active sites where HCl can be released
    Radical         Concentration of radicals formed on the polymer chains
    Prim_stab       Concentration of primary stabiliser in PVC
    Poly_deg        Concentration of degraded polymer (where degraded polymer
                    refers to double bonds that formed)
    Cross_link      Concentration of cross-links between polymer chains
    """

    HCl, LDH, Poly_active, Radical, Prim_stab, Poly_deg, Cross_link = Variables
    dHCl = -10*k3*HCl*LDH + k4*HCl*Poly_active + k5*Poly_active - k12*Area*HCl
    dLDH = -k3*HCl*LDH
    dPoly_active = -k4*HCl*Poly_active - k5*Poly_active
    dRadical = k4*HCl*Poly_active + k5*Poly_active - k6*Radical*Prim_stab \
        - k7*Radical - 2*k8*Radical
    dPrim_stab = -k6*Radical*Prim_stab
    dPoly_deg = k7*Radical
    dCross_link = k8*Radical

    return [dHCl,
            dLDH,
            dPoly_active,
            dRadical,
            dPrim_stab,
            dPoly_deg,
            dCross_link]

"Simulate the Metrastat"

Timespan = linspace(0, 120, 120)
Simulation = odeint(metrostat, initial, Timespan)
legendstr = ['HCl',
             'LDH',
             'Polymer active sites',
             'Radical',
             'Primary stabiliser',
             'Degraded polymer',
             'Cross-links']

plot.plot(Timespan, Simulation)
plot.title('Specie concentrations')
plot.xlabel('Time /min')
plot.ylabel('Concentration')
plot.legend(legendstr)
plot.close()

"Generate graphs seperately"

for i in range(7):
    plot.figure(i)
    plot.plot(Timespan, Simulation[:, i])
    plot.title(legendstr[i] + ' concentration')
    plot.xlabel('Time /min')
    plot.ylabel('Concentration')
    plot.savefig(legendstr[i] + '.pdf')
