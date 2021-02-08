import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
from uncertainties import unumpy as unp
from labtables import Table


def uscatter(x, y, add_line=False):
    """Scatter-plot arrays of uncertainties.ufloats, adding errorbars"""
    x_nom = unp.nominal_values(x)
    y_nom = unp.nominal_values(y)
    x_std = unp.std_devs(x)
    y_std = unp.std_devs(y)

    # plt.scatter(x_nom, y_nom)
    plt.errorbar(x_nom, y_nom, xerr=x_std, yerr=y_std, fmt='o')
    if add_line:
        slope, intercept = np.polyfit(x_nom, y_nom, 1)
        print(f'Plotting line with slope = {slope}, intercept = {intercept}')
        plt.plot(x_nom, slope * x_nom + intercept)

ress = (23, 34, 44, 55, 65)
paths = (f'voltages_{r}ohm.csv' for r in ress)

for path in paths:
    numbers, voltages = Table.read_csv(path)
    numbers = np.array(numbers)
    voltages = unp.uarray(voltages, 0.1)
    uscatter(numbers, unp.log(voltages), add_line=True)

plt.grid()
plt.xlabel('Номер пика $U(t)$', fontsize=14)
plt.ylabel('Логарифм пикового напряжения', fontsize=14)
plt.savefig('qfactor_peaks.png')

slopes = (0.150, 0.481, 0.715, 0.898, 0.916)
