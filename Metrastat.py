from __future__ import division
from numpy import linspace
from scipy.integrate import odeint
from matplotlib import pyplot as plot
from parameters import get_constants, get_initial

# set up differential model for the metrastat


def metrastat(variables, time, k12_vary=0):
    # constants
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12 = get_constants()
    if k12_vary > 0:
        k12 = k12_vary
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

    HCl, LDH, Poly_active, Radical, Prim_stab, Poly_deg, Cross_link = variables
    dHCl = -10*k3*HCl*LDH + k4*HCl*Poly_active + k5*Poly_active - k12*HCl
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

# simulate the metrastat and plot the concentration profiles of each specie

timespan = linspace(0, 120, 120)
initial = get_initial()
simulation = odeint(metrastat, initial, timespan)
legendstr = ['HCl',
             'LDH',
             'Polymer active sites',
             'Radical',
             'Primary stabiliser',
             'Degraded polymer',
             'Cross-links']

plot.plot(timespan, simulation)
plot.title('Specie concentrations')
plot.xlabel('Time /min')
plot.ylabel('Concentration')
plot.legend(legendstr)
