from __future__ import division
from data_refine import refine_max, get_file_names
from parameters import get_initial, get_constants
from fitting_one_set_params import fit_experimental
from numpy import array, dot
from Metrastat import metrastat
from numpy.linalg import lstsq
from scipy.integrate import odeint
from time import time
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import pandas

# get file names from experimental database
exp_data = get_file_names('Wimpie Data/Rheomix Results/')

# build an array of refined YI-data to fit using one set of parameters
time_to_fit = []
YI_to_fit = []
init_for_fit = get_initial('Reinhard Fit/')
cons_for_fit = get_constants('Reinhard Fit/')

# build an array of initial guesses to compare runtime
guesses = []

start = time()

for i, data in enumerate(exp_data):
    sample = pandas.read_csv(data, index_col='Time')
    sample = sample.dropna()

    # refine data to remove faulty data points
    new_time, new_YI = refine_max(sample)
    YI_to_fit.append((new_YI))
    time_to_fit.append(new_time)

    # get initial values for ODE's
    initial = init_for_fit[i]

    # get constants for ODE's
    constants = cons_for_fit[i]

    # assume k12 = 0.8 to get initial guesses
    concentration = odeint(metrastat, initial, sample.index,
                           args=(0.8, constants,))
    conc_mat = array(concentration)
    guess = lstsq(conc_mat, sample.YI)[0]
    x0 = list(guess)
    x0.append(0.8)
    guesses.append(x0)

# do a least-squares fit
params = fit_experimental(time_to_fit, YI_to_fit, init_for_fit,
                          guesses[0], cons_for_fit)

end = time()
print "Elapsed time: %f" % (end - start)

# plot each curve using the parameters determined by least-squares fit
params_vector = array((params['a'], params['b'], params['c'], params['d'],
                       params['e'], params['f'], params['g']), dtype=float)
rate_HCl = params['k12']


with PdfPages('fitting_results.pdf') as pdf:

    for i in range(len(time_to_fit)):
        # simulate the metrastat ODE
        concentration = odeint(metrastat, init_for_fit[i], time_to_fit[i],
                               args=(rate_HCl, cons_for_fit[i],))

        # plot YI using the result of the least-squares fit
        conc_mat = array(concentration)
        fit = dot(conc_mat, params_vector)

        # save each plot in a pdf page
        fig = plt.figure()
        path, fname = exp_data[i].rsplit('/', 1)
        sample, ftype = fname.split('.')

        plt.title('Fit for sample ' + sample)
        plt.xlabel('Time /s')
        plt.ylabel('YI')
        plt.plot(time_to_fit[i], YI_to_fit[i],
                 time_to_fit[i], fit)
        plt.legend(['Experimental', 'Fit'], loc=0)
        pdf.savefig()

    pdf.close()