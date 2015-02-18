import json


def get_constants():
    with open('cons.json') as f:
        cons = json.load(f)

    return [cons['k1'],
            cons['k2'],
            cons['k3'],
            cons['k4'],
            cons['k5'],
            cons['k6'],
            cons['k7'],
            cons['k8'],
            cons['k9'],
            cons['k10'],
            cons['k11'],
            cons['k12']]


def get_initial():
    with open('initial.json') as f:
        initial = json.load(f)

    return [initial['HCl_0'],
            initial['LDH_0'],
            initial['Poly_active_0'],
            initial['Radical_0'],
            initial['Prim_stab_0'],
            initial['Poly_deg_0'],
            initial['Cross_link_0']]