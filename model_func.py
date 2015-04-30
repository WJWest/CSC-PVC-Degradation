from time import time
from data_refine import refine_YI
from fitting_YI_all_models import fit_experimental

import pandas


def metrastat_model(exp_data, initial_conditions, rate_constants,
                    refine_extended=False, one_set_params=False):

    start = time()

    # refine data to remove faulty data points, and store in a single list
    all_times = []
    all_YI = []

    for data in exp_data:
        sample = pandas.read_csv(data, index_col='Time')
        sample = sample.dropna()

        if refine_extended:
                new_YI, new_time = refine_YI(sample, extended=True)
        else:
            new_YI, new_time = refine_YI(sample)

        # update the single list that will be used in the fitting
        all_times.append(new_time)
        all_YI.append(new_YI)

    # fit using only one set of parameters
    if one_set_params:
        quadratic, params, error = fit_experimental(all_times, all_YI,
                                                    initial_conditions,
                                                    rate_constants,
                                                    one_set_params=True)

    # fit each curve individually
    else:
        params = []
        error = []
        quadratic = []

        for i in range(len(exp_data)):
            quadratic_temp, params_temp, error_temp = \
                fit_experimental(all_times[i], all_YI[i],
                                 initial_conditions[i], rate_constants[i])

            # update results
            params.append(params_temp)
            error.append(error_temp)
            quadratic.append(quadratic_temp)

    stop = time()
    print "elapsed time = %f min" % ((stop - start)/60)
    return [params, error, quadratic, all_times, all_YI]
