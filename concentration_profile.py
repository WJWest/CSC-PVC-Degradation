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

for i, data in enumerate(exp_data):
    # simulate the metrastat
    sample = pd.read_csv(data, index_col='Time')
    sample.dropna()
    YI, time = refine_YI(sample)

    constants = all_constants[i]
    initial = all_initial[i]

    conc = odeint(metrastat, initial, time, args=(k12, constants))
    conc_mat = array(conc, dtype=float)

    # plot concentration profile
    _, fname = data.rsplit('/', 1)
    sample_name, _ = fname.split('.')

    plt.figure(i)
    plt.title('Fit for sample ' + sample_name)
    plt.xlabel('Time /min')
    plt.ylabel('Concentration')
    plt.plot(time, conc_mat)
    plt.legend(['HCl', 'LDH', 'Active sites', 'Radical', 'Primary Stabiliser',
                'Double bonds', 'Cross-link'], loc=0)

    # save plot
    fname = set_filename('Concentration Profiles/' + sample_name + '.svg')
    plt.savefig(fname)
    plt.show()
