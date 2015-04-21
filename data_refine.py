# procedure to take raw experimental data with errors and refine it

from directories import set_filename

import glob
import os
import pandas


# extract all file names
def get_csv(extension):
    # access database with names of available results
    fname = set_filename(extension)
    directory = glob.glob(os.path.join(fname, '*.csv'))

    return directory


def get_xlsx(extension):
    fname = set_filename(extension)
    directory = glob.glob(os.path.join(fname, '*.xlsx'))

    return directory


def get_file_names(extension, Ca_Only=False):
    directory = get_xlsx(extension)
    results = pandas.read_excel(directory[0], 0, index_col='Date')
    results = results.dropna(subset=['Time'])

    # generate list with file names of available results
    files = []
    results['Sample'] = results['Sample'] + '.csv'

    if not(Ca_Only):
        for file_name in results['Sample']:
            files.append(set_filename('Wimpie Data/Metrastat Results/'
                                      + file_name))
    else:
        for file_name in results['Sample']:
            if file_name[0:2] == 'Ca':
                files.append(set_filename('Wimpie Data/Metrastat Results/'
                                          + file_name))

    return files


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


# remove faulty data after max YI
def refine_max(raw_data):
    " raw_data must be a pandas dataframe "

    # find maximum YI in experimental data
    max_YI = raw_data.YI == raw_data.YI.max()

    # get time index where maximum YI occurs
    max_Index = raw_data[max_YI].index

    # slice the data after maximum YI
    trunc = raw_data.index < max_Index

    return [raw_data[trunc].index,
            raw_data[trunc]['YI']]
