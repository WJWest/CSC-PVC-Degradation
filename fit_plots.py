from data_refine import get_file_names, refine_YI
from parameters import get_initial, get_constants
from scipy.integrate import odeint
from Metrastat import metrastat
from matplotlib import pyplot as plt
from numpy import array
from directories import set_filename

import pandas as pd

# get file names
exp_data = get_file_names('Wimpie Data/Rheomix Results/', sample='Mg')

# load initial conditions
all_initial = get_initial('Reinhard Fit/')

# load rate constants
all_constants = get_constants('Reinhard Fit/')

k12 = 0

Mg = [20.1, 110.4, 90.7, -39, -3.2]
Ca = [27.6, 101.6, 78.4, -34.1, 18.3]

for i, data in enumerate(exp_data):
    # simulate the metrastat
    sample = pd.read_csv(data, index_col='Time')
    sample.dropna()
    YI, time = refine_YI(sample)

    constants = all_constants[i]
    initial = all_initial[i]

    conc = odeint(metrastat, initial, time, args=(k12, constants))
    conc_mat = array(conc, dtype=float)

    fit = Mg[0]*conc_mat[:,1] + \
          Mg[1]*conc_mat[:,5] + \
          Mg[2]*conc_mat[:,6] + \
          Mg[3]*conc_mat[:,5]**2 + \
          Mg[4]

    # plot concentration profile
    _, fname = data.rsplit('/', 1)
    sample_name, _ = fname.split('.')

    plt.figure(i)
    plt.title('Fit for sample ' + sample_name)
    plt.xlabel('Time /min')
    plt.ylabel('Concentration')
    plt.plot(time, YI)
    plt.plot(time, fit)
    plt.legend(['Experimental', 'Fit'], loc=0)

    # save plot
    fname = set_filename('YI Profiles/' + sample_name + '.svg')
    plt.savefig(fname)
    plt.show()
