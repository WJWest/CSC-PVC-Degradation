"""
This function receives an array with multiple rows (but one column)
It will arrange each row next to each other to return a single row

The second argument is the array (allready converted to one row) to
which the function will add the current converted array
"""
from numpy import array


def one_row(multi_rows, converted):
    result = []

    for entry in converted:
        result.append(entry)

    for entry in multi_rows:
        result.append(entry)

    return array(result)
