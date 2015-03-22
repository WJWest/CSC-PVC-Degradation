# do a least-squares fit to determine HCl removal rate constants such to
# minimize the absolute error (Levenberg-Marquard algorithm)

from __future__ import division
from Metrastat import metrastat
from numpy import array, dot
from scipy.integrate import odeint
from lmfit import minimize, Parameters
from directories import set_filename


def fit_experimental(time, YI, initial, x0, iteration, constants):
    from lmfit import fit_report

    def obj_func(params, time, YI):
        # unpack parameters to be fitted
        v = params.valuesdict()

        # create vector for lstsq solution
        constant_vector = array((v['a'], v['b'], v['c'], v['d'], v['e'],
                                 v['f'], v['g']), dtype=float)

        concentrations = odeint(metrastat, initial, time,
                                args=(v['k12'], constants))
        conc_mat = array(concentrations)

        return dot(conc_mat, constant_vector) - array(YI, dtype=float)

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
    result = minimize(obj_func, params, args=(time, YI))

    # calculate weighted error
    error = sum(result.residual**2)
    npoints = len(time)
    weighted = error/npoints
    print "error = " + str(weighted)

    # generate the fitting report
    fname = set_filename('Fitting results/') + 'Fit' + \
        str(iteration) + ' report.txt'

    report = open(fname, "w")
    report.write('Fitting report\n\n')

    # unpack reaction constants
    k3, k4, k5, k6, k7, k8 = constants
    report.write('Rate constants used:\n')

    for i, k in enumerate(constants):
        report.write('k' + str(i+3) + '\t' + str(k) + '\n')

    report.write('\nFitted parameters:\n')
    fit_results = params.valuesdict()

    for fit_param in fit_results:
        report.write(fit_param + '\t' + str(fit_results[fit_param]) + '\n')

    report.write('\nWeighted error:')
    report.write('\n' + str(weighted) + '\n')

    report.write('\nAdditional comments:\n')
    report.write(fit_report(params))
    report.close()

    return [array(YI, dtype=float) + result.residual,
            fit_results,
            weighted]
