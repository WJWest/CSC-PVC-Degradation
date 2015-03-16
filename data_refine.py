# procedure to take raw experimental data with errors and refine it

import json
import glob
import os

# read configuration file and expand ~ to user directory
with open('config.json') as f:
    config = json.load(f)

datadir = os.path.expanduser(config['datadir'])


# extract all file names
def get_csv(extension):
    datadir_extended = datadir + extension
    return glob.glob(os.path.join(datadir_extended, '*.csv'))


# remove faulty data after max YI
def refine_YI(raw_data): 
    " raw_data must be a pandas dataframe "

    # find maximum YI in experimental data
    max_YI = raw_data.YI == raw_data.YI.max()

    # get time index where maximum YI occurs
    max_Index = raw_data[max_YI].index
    
    # slice the data after maximum YI
    trunc = raw_data.index > max_Index

    # update faulty data to remain at the maximum YI
    raw_data['YI'][trunc] = raw_data.YI.max()

    return raw_data['YI']    
