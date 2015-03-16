# do a least-squares fit to determine HCl removal rate constants such to
# minimize the absolute error (Levenberg-Marquard algorithm)

from __future__ import division
from Metrastat import metrastat
from numpy import array, dot
from scipy.integrate import odeint
from lmfit import minimize, Parameters


def fit_experimental(time, YI, initial, x0):
    from lmfit import report_fit

    def obj_func(params, time, YI):
        # unpack parameters to be fitted
        v = params.valuesdict()

        # create vector for lstsq solution
        constant_vector = array((v['a'], v['b'], v['c'], v['d'], v['e'],
                                 v['f'], v['g']), dtype=float)

        concentrations = odeint(metrastat, initial, time, args=(v['k12'],))
        conc_mat = array(concentrations)

        return dot(conc_mat, constant_vector) - array(YI, dtype=float)

    # set initial parameter values
    params = Parameters()

    #          (Name,   Value,  Vary,   Min,    Max,    Expr)
    params.add_many(('a',    x0[0],  True,   None,   None,   None),
                    ('b',    x0[1],  True,   None,   None,   None),
                    ('c',    x0[2],  True,   None,   None,   None),
                    ('d',    x0[3],  True,   None,   None,   None),
                    ('e',    x0[4],  True,   None,   None,   None),
                    ('f',    x0[5],  True,   None,   None,   None),
                    ('g',    x0[6],  True,   None,   None,   None),
                    ('k12',  x0[7],  True,   None,   None,   None))

    # do fit with leastsq model
    result = minimize(obj_func, params, args=(time, YI))
    print report_fit(params)

    return array(YI, dtype=float) + result.residual
