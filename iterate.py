"""
The yellowing-index (YI) will be modelled as a f([specie concentrations])

A quadratic function is proposed. This module will evaluate every possible
combination of powers that each specie may have such that a quadratic equation
is still achieved
"""
from itertools import combinations, combinations_with_replacement, chain


def all_powers(Nspecies, order, Ncoeffs):
    possiblevariables = []

    for o in xrange(order):
        for order_combinations in combinations_with_replacement(xrange(Nspecies), o+1):
            possiblevariables.append(order_combinations)

    power_list = []
    for power in combinations(chain(possiblevariables), Ncoeffs):
        power_list.append(power)

    return power_list
