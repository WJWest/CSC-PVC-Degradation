from __future__ import division
from data_refine import get_csv, refine_YI
from parameters import get_initial, get_constants
from fitting_YI import fit_experimental
from numpy import array
from matplotlib import pyplot as plot
from Metrastat import metrastat
from numpy.linalg import lstsq
from scipy.integrate import odeint
from time import time
from directories import set_filename

import pandas

# get file names from experimental database
exp_data = get_csv('Harry Data/')

# save the least-squares solution after every fit
soln = []

# loop through experimental data files
start = time()
for i, data in enumerate(exp_data):
    print 'Busy with fit: %d' % (i)

    sample = pandas.read_csv(data, index_col='Time')
    sample = sample.dropna()

    # refine data to remove faulty data points
    new_YI = refine_YI(sample)

    # get initial values for ODE's
    initial = get_initial('Reinhard Fit/', i)

    # get constants
    constants = get_constants('Reinhard Fit/', i)
    ldh = get_constants('Reinhard Fit/', i, True)

    # assume k12 = 0.8 to get initial guesses
    concentration = odeint(metrastat, initial, sample.index,
                           args=(0.8, constants,))
    conc_mat = array(concentration)
    guess = lstsq(conc_mat, sample.YI)[0]
    x0 = list(guess)
    x0.append(0.8)

    # do a least-squares fit
    fit, params, error = fit_experimental(sample.index, sample.YI,
                                          initial, x0, i, constants)

    # update solution list
    param_dict = pandas.Series(params)
    add_dict = pandas.Series({"error": error,
                              "LDH": ldh})
    final_dict = param_dict.append(add_dict)
    soln.append(final_dict)

    # plot the least-squares fit
    plot.figure(i)
    plot.plot(sample.index, sample.YI,
              sample.index, fit)
    fname = set_filename('Fitting results/') + 'Fit' + str(i) + '.jpg'
    plot.savefig(fname)
    plot.close()

stop = time()
print 'Elapsed time = %f' % (stop - start)

# save results to a .csv database
results_df = pandas.DataFrame(soln)
fname = set_filename('Fitting results/') + 'Fitting_resutls.csv'
pandas.DataFrame.to_csv(results_df, fname)

# group the error by LDH concentration
ldh_df = results_df[['LDH', 'error']]

# add the total error per group of LDH concentration
total_error = ldh_df.groupby('LDH').sum()

# get the number of a specific LDH concentration that was fitted
ldh_count = ldh_df.groupby('LDH').count()

# calculate the average error for each group of LDH concentration
avg_error = total_error['error']/ldh_count['error']
avg_error.plot(kind='bar')
