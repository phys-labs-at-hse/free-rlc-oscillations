import labtables


paths = (f'voltages_{r}ohm.csv' for r in (23, 34, 44, 55, 65))

for path in paths:
    labtables.Table(
        *labtables.read_csv(path),
        colnames=('Номер пика', 'Амплитуда, дел.')
    ).write_latex('latex_tables/' + path.replace('csv', 'tex'))
