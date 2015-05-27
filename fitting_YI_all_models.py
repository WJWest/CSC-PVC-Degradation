# this module will evaluate the possible quadratic expressions that exists
# when the yellowing-index (YI) is expressed as a function of the specie
# concentrations present during degradation. The expression that results in
# the smallest error will be determined

from __future__ import division
from Metrastat import metrastat
from numpy import array, ones
from scipy.integrate import odeint
from lmfit import minimize, Parameters
from iterate import all_powers
from objective import one_row


def fit_experimental(time, YI, initial, constants, one_set_params=False):
    # print the time each time a smaller error has been found
    if one_set_params:
        from time import time as tm
        start = tm()

    min_error = 10e10
    power_list = all_powers(4, 2, 4)

    nr_comb = len(power_list)

    for iteration, powers in enumerate(power_list):
        print 'Combination %d/%d' % (iteration + 1, nr_comb)

        def obj_func(params, time, YI):
            # unpack parameters to be fitted
            v = params.valuesdict()

            if one_set_params:
                # join each fit into a single residual array
                all_YI = array([])
                all_fits = array([])

                for nr in range(len(time)):
                    # simulate the metrastat
                    concentrations = odeint(metrastat, initial[nr], time[nr],
                                            args=(v['k12'], constants[nr]))

                    conc_mat = array(concentrations, dtype=float)
        
                    # build an array in which each specie correlates to an index
                    LDH = conc_mat[:, 1]
                    poly_active = conc_mat[:, 2]
                    deg_poly = conc_mat[:, 5]
                    cross_link = conc_mat[:, 6]
                    specie_mat = array([LDH, poly_active, deg_poly, 
                                        cross_link], dtype=float)
        
                    # build an array which will contain the species for each coefficient
                    # in the form a[array index 0] + b[array index 1]
                    func_array = array([ones(len(YI[nr])),                 # LDH
                                        ones(len(YI[nr])),                 # poly_active
                                        ones(len(YI[nr])),                 # poly_deg
                                        ones(len(YI[nr]))], dtype=float)   # cross_link
        
                    # apply the coeffs in the powers list
                    for i, coeffs in enumerate(powers):
                        for specie_power in coeffs:
                            func_array[i] *= specie_mat[specie_power]
        
                    fit = v['a']*func_array[0] + \
                          v['b']*func_array[1] + \
                          v['c']*func_array[2] + \
                          v['d']*func_array[3] + \
                          v['e']

                    # update residual function
                    all_YI = one_row(YI[nr], all_YI)
                    all_fits = one_row(fit, all_fits)

                return all_YI - all_fits

            else:                
                # simulate the metrastat
                concentrations = odeint(metrastat, initial, time,
                                        args=(v['k12'], constants))
                conc_mat = array(concentrations, dtype=float)
    
                # build an array in which each specie correlates to an index
                LDH = conc_mat[:, 1]
                poly_active = conc_mat[:, 2]
                deg_poly = conc_mat[:, 5]
                cross_link = conc_mat[:, 6]
                specie_mat = array([LDH, poly_active, deg_poly, 
                                    cross_link], dtype=float)
    
                # build an array which will contain the species for each coefficient
                # in the form a[array index 0] + b[array index 1]
                func_array = array([ones(len(YI)),                 # LDH
                                    ones(len(YI)),                 # poly_active
                                    ones(len(YI)),                 # poly_deg
                                    ones(len(YI))], dtype=float)   # cross_link
    
                # apply the coeffs in the powers list
                for i, coeffs in enumerate(powers):
                    for specie_power in coeffs:
                        func_array[i] *= specie_mat[specie_power]
    
                return v['a']*func_array[0] + \
                    v['b']*func_array[1] + \
                    v['c']*func_array[2] + \
                    v['d']*func_array[3] + \
                    v['e'] - array(YI, dtype=float)

        # set initial parameter values
        params = Parameters()

        #               (Name,   Value, Vary,   Min,    Max,    Expr)
        params.add_many(('a',    0,     True,   None,   None,   None),
                        ('b',    0,     True,   None,   None,   None),
                        ('c',    0,     True,   None,   None,   None),
                        ('d',    0,     True,   None,   None,   None),
                        ('e',    0,     True,   None,   None,   None),
                        ('k12',  0,     True,   0,      None,   None))

        # do fit with leastsq model
        result = minimize(obj_func, params, args=(time, YI))

        # calculate weighted error
        error = sum(result.residual**2)
        npoints = len(time)
        weighted = error/npoints

        # test for smallest error
        if weighted < min_error:
            min_error = weighted
            best_params = params.valuesdict()
            best_quadratic = powers
            print 'error: %f' % weighted
            try:
                elapsed = (tm() - start)/60
                print "elapsed time = %f min" % elapsed
                remain = elapsed/(iteration + 1)*(nr_comb - iteration - 1)
                print "time remaining = %f min" % remain
            except:
                pass

    return [best_quadratic, best_params, min_error]
