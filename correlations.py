from data_refine import refine_YI, get_file_names
from matplotlib import pyplot as plt

import pandas as pd

exp_data = get_file_names('Wimpie Data/Rheomix Results/', sample='Mg')

legend = []
evaluate = list(exp_data[i] for i in (0, 2, 6, 10))

for data in evaluate:
    sample = pd.read_csv(data, index_col='Time')
    sample = sample.dropna()

    YI, Time = refine_YI(sample)
    _, fname = data.rsplit('/', 1)
    name, _ = fname.split('.')
    legend.append(name)

    plt.plot(Time, YI, label=name)

plt.legend(legend, loc=0)
