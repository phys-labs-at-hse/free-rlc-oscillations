import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
from uncertainties import unumpy as unp


def uscatter(x, y, add_line=False):
    """Scatter-plot arrays of uncertainties.ufloats, adding errorbars"""
    x_nom = unp.nominal_values(x)
    y_nom = unp.nominal_values(y)
    x_std = unp.std_devs(x)
    y_std = unp.std_devs(y)

    plt.errorbar(x_nom, y_nom, xerr=x_std, yerr=y_std, fmt='o')
    if add_line:
        slope, intercept = np.polyfit(x_nom, y_nom, 1)
        print(f'Plotting line with slope = {slope}, intercept = {intercept}')
        plt.plot(x_nom, slope * x_nom + intercept)


cs = np.array([21.86, 33.23, 50.72, 70.83, 100.3, 223.6, 477.5, 927.7,])
cs = unp.uarray(cs, cs * 0.02)

periods = np.array([77, 92, 110, 130, 160, 240, 340, 480,])

periods = unp.uarray(periods, periods * 0.05)

uscatter(unp.sqrt(cs), periods, True)
plt.grid()
plt.xlabel('$\sqrt{C}$, нФ$^{0.5}$', fontsize=14)
plt.ylabel('Периоды, мкс', fontsize=14)
plt.savefig('check_periods.png')

# Slope = 2π * √L ; 15.7 converted to SI.
slope =  15.7 / 1e6 * np.sqrt(1e9)
L = (slope / (2 * np.pi))**2
print(f'L = {L * 1e3} mH')
