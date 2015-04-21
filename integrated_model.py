from __future__ import division
from data_refine import get_file_names, refine_YI
from parameters import get_initial, get_constants
from fitting_YI_all_models import fit_experimental
from numpy import array
from matplotlib import pyplot as plt
from Metrastat import metrastat
from numpy.linalg import lstsq
from scipy.integrate import odeint
from time import time
from directories import set_filename
from matplotlib.backends.backend_pdf import PdfPages

import pandas

# get file names from experimental database
exp_data = get_file_names('Wimpie Data/Rheomix Results/', Ca_Only=False)

# save the least-squares solution after every fit
soln = []

# get initial values for ODE's
all_initial = get_initial('Reinhard Fit/')

# get constants as determined by Fechter's fit
all_constants = get_constants('Reinhard Fit/')

# loop through experimental data files
start = time()

with PdfPages('quadratic.pdf') as pdf:

    for i, data in enumerate(exp_data):
        print 'Busy with fit: %d' % (i)

        sample = pandas.read_csv(data, index_col='Time')
        sample = sample.dropna()

        # refine data to remove faulty data points
        new_YI = refine_YI(sample)

        # get initial values
        initial = all_initial[i]
        ldh = initial[1]

        # get constants
        constants = all_constants[i]

        # assume k12 = 0.8 to get initial guesses
        concentration = odeint(metrastat, initial, sample.index,
                               args=(0.8, constants,))
        conc_mat = array(concentration)
        guess = lstsq(conc_mat, sample.YI)[0]
        x0 = list(guess)
        x0.append(0.8)

        # do a least-squares fit
        fit, params, error = fit_experimental(sample.index, new_YI,
                                              initial, x0, i, constants)

        # update solution list
        param_dict = pandas.Series(params)
        add_dict = pandas.Series({"error": error,
                                  "LDH": ldh})
        final_dict = param_dict.append(add_dict)
        soln.append(final_dict)

        # plot YI using the result of the least-squares fit
        fig = plt.figure()
        path, fname = data.rsplit('/', 1)
        sample_name, ftype = fname.split('.')

        plt.title('Fit for sample ' + sample_name)
        plt.xlabel('Time /s')
        plt.ylabel('YI')
        plt.plot(sample.index, new_YI,
                 sample.index, fit)
        plt.legend(['Experimental', 'Fit'], loc=0)
        pdf.savefig()
        plt.close()

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
