# set up differential model for the metrastat


def metrastat(variables, time, k12, constants):
    # unpack rate constants
    k3, k4, k5, k6, k7, k8 = constants

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
