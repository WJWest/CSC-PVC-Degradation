# do a least-squares fit to determine HCl removal rate constants such to
# minimize the absolute error (Levenberg-Marquard algorithm)

from __future__ import division
from Metrastat import metrastat
from numpy import array, ones
from scipy.integrate import odeint
from lmfit import minimize, Parameters
from iterate import all_powers


def fit_experimental(time, YI, initial, x0, iteration, constants):

    """
    Species to be used
        *deg_poly
        *cross_link

    The yellowing-index (YI) will be modelled as a f([deg_poly], [cross_link])

    All the possibilities of a quadratic function will be considered
    """

    min_error = 10e5
    min_residual = array(YI, dtype=float)
    power_list = all_powers(2, 2, 2)

    nr_comb = len(power_list)

    for iteration, powers in enumerate(power_list):
        print 'Combination %d/%d' % (iteration, nr_comb)

        for i, coeffs in enumerate(powers):

            def obj_func(params, time, YI):
                # unpack parameters to be fitted
                v = params.valuesdict()

                # simulate the metrastat
                concentrations = odeint(metrastat, initial, time,
                                        args=(v['k12'], constants))
                conc_mat = array(concentrations, dtype=float)

                # build an array in which each specie correlates to an index
                deg_poly = conc_mat[:, 5]
                cross_link = conc_mat[:, 6]
                specie_mat = array([deg_poly, cross_link], dtype=float)

                # build an array which will contain the species for each coefficient
                # in the form a[array index 0] + b[array index 1]
                func_array = array([ones(len(YI)), ones(len(YI))], dtype=float)

                # apply the coeffs in the powers list
                for specie_power in coeffs:
                    func_array[i] *= specie_mat[specie_power]

                return v['a']*func_array[0] + v['b']*func_array[1] + v['c']\
                    - array(YI, dtype=float)

            # set initial parameter values
            params = Parameters()

            #               (Name,   Value,  Vary,   Min,    Max,    Expr)
            params.add_many(('a',    x0[0],  True,   None,   None,   None),
                            ('b',    x0[1],  True,   None,   None,   None),
                            ('c',    x0[2],  True,   None,   None,   None),
        #                    ('d',    x0[3],  True,   None,   None,   None),
        #                    ('e',    x0[4],  True,   None,   None,   None),
        #                    ('f',    x0[5],  True,   None,   None,   None),
        #                    ('g',    x0[6],  True,   None,   None,   None),
                            ('k12',  x0[7],  True,   0,      None,   None))

            # do fit with leastsq model
            result = minimize(obj_func, params, args=(time, YI))

            # calculate weighted error
            error = sum(result.residual**2)
            npoints = len(time)
            weighted = error/npoints

            # test for smallest error
            if weighted < min_error:
                min_error = weighted
                min_residual = result.residual
                fit_results = params.valuesdict()
                print 'error: %f' % weighted

    return [array(YI, dtype=float) + min_residual,
            fit_results,
            weighted]
