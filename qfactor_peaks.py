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


ress = np.array((23, 34, 44, 55, 65))
paths = (f'voltages_{r}ohm.csv' for r in ress)

for path in paths:
    numbers, voltages = Table.read_csv(path)
    numbers = np.array(numbers)
    voltages = unp.uarray(voltages, 0.1)
    uscatter(numbers, unp.log(voltages), add_line=True)
print()

plt.grid()
plt.title('По пикам', fontsize=16)
plt.xlabel('Номер пика $U(t)$', fontsize=14)
plt.ylabel('Логарифм пикового напряжения', fontsize=14)
plt.savefig('qfactor_peaks.png')
plt.close()

slopes = np.array((0.370, 0.486, 0.614, 0.797, 0.914,))

# Moving to the spiral method
voltages_tuple = (
    (9, 6.6, 4.8, 3.4, 2.4, 1.6,),
    (10.4, 7, 4.5, 2.8, 1.8,),
    (8.2, 4.7, 2.6, 1.4,),
    (7.6, 3.7, 1.7, 0.8,),
)

for voltages in voltages_tuple:
    voltages = unp.uarray(voltages, 0.1)
    numbers = np.array(range(1, len(voltages) + 1))
    uscatter(numbers, unp.log(voltages), add_line=True)

plt.grid()
plt.title('По спирали', fontsize=16)
plt.xlabel('Номер пика $U(t)$', fontsize=14)
plt.ylabel('Логарифм пикового напряжения', fontsize=14)
plt.savefig('qfactor_peaks_spiral.png')
plt.close()

slopes_spiral = np.array((0.343, 0.442, 0.589, 0.753,))

# Compare the decrement coefs from different methods.
# They should be proportional to R.
plt.scatter(ress, slopes, label='По пикам')
plt.scatter(ress[:-1], slopes_spiral, label='По спирали')
slope, intercept = np.polyfit(ress[:-1], slopes_spiral, 1)
plt.plot(ress, slope * ress + intercept, color='r')
plt.plot(ress, 2 * np. pi / 440 * ress + intercept, color='r')
plt.grid()
plt.legend()
plt.xlabel('Сопротивление реостата', fontsize=14)
plt.ylabel('Декремент затухания', fontsize=14)
plt.savefig('qfactor_prop_r.png')
plt.close()

print(f'Slope is {slope}, while it must be  2π / R_cr = 2π / 440 = {2 * np.pi / 440}')
