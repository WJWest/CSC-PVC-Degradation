""""
The Rheomix measures torque and temperature. These curves was fitted using a
model based on the kinects of PVC degradation. As a result from the fit the
relevant rate constants could be determined.

This module will read the constants as determined by each fitting of the
Rheomix data as well as the initial conditions present in each fitting.
"""

from data_refine import get_csv

import pandas
import json


# read a single row from the database containing
# the results of the Rheomix fitings
def get_row(extension, row):
    fname = get_csv(extension)

    # open the database containing the constants fitted via the Rheomix
    df_expdata = pandas.read_csv(fname[0])

    # return the relevant row of the dataframe
    return df_expdata.iloc[row]


def get_constants(extension, row, LDH=False):
    constants = get_row(extension, row)

    if LDH:
        return constants['LDH_0']
    else:
        return [constants['k3'],
                constants['k4'],
                constants['k5'],
                constants['k6'],
                constants['k7'],
                constants['k8']]


def get_initial(extension, row):
    # read the initial concentrations
    with open('initial.json') as f:
        initial = json.load(f)

    LDH = get_constants(extension, row, True)
    return [initial['HCl_0'],
            LDH,
            initial['Poly_active_0'],
            initial['Radical_0'],
            initial['Prim_stab_0'],
            initial['Poly_deg_0'],
            initial['Cross_link_0']]
