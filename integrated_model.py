from __future__ import division
from data_refine import get_csv, refine_YI
from parameters import get_initial
from fitting_YI import fit_experimental
from numpy import load
from matplotlib import pyplot as plot

import pandas

# get file names from experimental database
exp_data = get_csv('Harry Data/')

# use first experiment as a sample to fit
sample = pandas.read_csv(exp_data[0], index_col='Time')

# refine data to remove faulta data points
new_YI = refine_YI(sample)

# get initial guesses
x0 = load('soln.npy')

# get initial values for ODE's
initial = get_initial()

# do a least-squares fit
fit = fit_experimental(sample.index, sample.YI, initial, x0)

plot.plot(sample.index, sample.YI,
          sample.index, fit)
