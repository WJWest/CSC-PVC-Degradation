# do a least-squares fit to determine HCl removal rate constants such to
# minimize the absolute error (Levenberg-Marquard algorithm)

from __future__ import division
from Metrastat import metrastat
from numpy import array, dot
from scipy.integrate import odeint
from lmfit import minimize, Parameters
from objective import one_row


def fit_experimental(time, YI, initial, x0, constants):

    def obj_func(params, time, YI):
        # unpack parameters to be fitted
        v = params.valuesdict()

        # create vector for lstsq solution
        constant_vector = array((v['a'], v['b'], v['c'], v['d'], v['e'],
                                 v['f'], v['g']), dtype=float)

        # join each fit into a single residual array
        all_YI = array([])
        all_fits = array([])

        for i in range(len(time)):
            print 'Busy with fit %d' % (i)

            # simulate the Metrastat
            concentrations = odeint(metrastat, initial[i], time[i],
                                    args=(v['k12'], constants[i]))

            # use the simulation to estimate the YI
            fit = dot(array(concentrations), constant_vector)

            # update residual function
            all_YI = one_row(YI[i], all_YI)
            all_fits = one_row(fit, all_fits)

        print '\n\n\nNext iteration:\n\n'

        return all_YI - all_fits

    # set initial parameter values
    params = Parameters()

    #               (Name,   Value,  Vary,   Min,    Max,    Expr)
    params.add_many(('a',    x0[0],  True,   None,   None,   None),
                    ('b',    x0[1],  True,   None,   None,   None),
                    ('c',    x0[2],  True,   None,   None,   None),
                    ('d',    x0[3],  True,   None,   None,   None),
                    ('e',    x0[4],  True,   None,   None,   None),
                    ('f',    x0[5],  True,   None,   None,   None),
                    ('g',    x0[6],  True,   None,   None,   None),
                    ('k12',  x0[7],  True,   None,   None,   None))

    # do fit with leastsq model
    minimize(obj_func, params, args=(time, YI))

    return params.valuesdict()
