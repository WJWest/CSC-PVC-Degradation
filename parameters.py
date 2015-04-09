""""
The Rheomix measures torque and temperature. These curves were fitted using a
model based on the kinects of PVC degradation. As a result from the fit the
relevant rate constants could be determined.

This module will read the constants as determined by each fitting of the
Rheomix data as well as the initial conditions present in each fitting.
"""

from data_refine import get_csv

import pandas
import json


def get_constants(extension):
    fname = get_csv(extension)

    df_cons = pandas.read_csv(fname[0], index_col=0)
    return df_cons[[2, 3, 4, 5, 6, 7]].values


def get_initial(extension):
    # read the initial concentrations
    with open('initial.json') as f:
        initial = json.load(f)

    # read the initial LDH concetrations
    fname = get_csv(extension)

    df_cons = pandas.read_csv(fname[0], index_col=0)
    LDH_0 = df_cons['LDH_0'].values

    # generate list with initial values
    initial_list = []

    for ldh in LDH_0:
        initial_list.append([initial['HCl_0'],
                             ldh,
                             initial['Poly_active_0'],
                             initial['Radical_0'],
                             initial['Prim_stab_0'],
                             initial['Poly_deg_0'],
                             initial['Cross_link_0']])

    return initial_list
