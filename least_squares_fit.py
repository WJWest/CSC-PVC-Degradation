# use an estimate for HCl removal rate constant (k=0.8) to do a least-squares fiting

from Metrastat import metrastat
from numpy import array, dot, save
from scipy.integrate import odeint
from matplotlib import pyplot as plot
from parameters import get_initial
from numpy.linalg import lstsq
from data_refine import get_csv

import pandas


# get initial values for numerical integration
initial = get_initial()

# get experimental data
exp_file = get_csv('lstsq fit/')
exp_data = pandas.read_csv(exp_file[0])

# do numerical integration (use same time and points as in data sample)
concentration = odeint(metrastat, initial, exp_data.Time, args=(0.8,))

# determine leat-squares solution
conc_mat = array(concentration)
soln = lstsq(conc_mat, exp_data.YI)

# save the parameters determined in least-squares fit
mat = list(soln[0])
mat.append(0.8)
save('soln', mat)

# use least square solution to fit the data
fit = dot(conc_mat, soln[0])

# plot the fit and original data
plot.figure(0)
plot.plot(exp_data.Time, exp_data.YI,
          exp_data.Time, fit)
plot.legend(['Experimental data', 'Least squares fit'], loc=4)
plot.title('Least squares fit of degraded PVC colour data')
plot.xlabel('Time')
plot.ylabel('YI')
