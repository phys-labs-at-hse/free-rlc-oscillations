class Table:
    def __init__(self, *columns, colnames=None):
        self.columns = columns

        if colnames:
            self.colnames = colnames
        else:
            self.colnames = (f'col{i}' for i in range(len(columns)))

        if not len(set(map(len, columns))) == 1:
            raise ValueError('Columns have different lengths.')

    def rows(self):
        """Return str array representing the table rows."""
        rows = []
        rows.append(','.join(self.colnames))
        for row in zip(*self.columns):
            rows.append(','.join(map(str, row)))
        return rows

    def __repr__(self):
        return '\n'.join(self.rows())

    def add_row_numbers(self):
        return Table(range(1, len(self.columns[0]) + 1),
                     *self.columns,
                     colnames=('№', *self.colnames))

    def to_csv(self, show_row_numbers=False):
        """Return given table as a multiline string in csv format."""
        if show_row_numbers:
            return self.add_row_numbers().__repr__()
        else:
            return self.__repr__()

    def write_csv(self, filepath, show_row_numbers=False):
        """Write given table to file in csv format."""
        if not filepath.endswith('.csv'):
            raise ValueError('Filepath extension is not ".csv".')
        with open(filepath, 'x') as file:
            file.write(self.to_csv(show_row_numbers=show_row_numbers))

    def to_latex(self, show_row_numbers=False):
        """Return given table as a string in the LaTeX tabular format."""
        table_copy = self.add_row_numbers() if show_row_numbers else self
        line_ending = r' \\ \hline' + '\n'

        result = r'\begin{tabular}{|'
        for i in range(len(table_copy.columns)):
            result += 'c|'
        result += '}' + '\n' + r'\hline' + '\n'

        result += ' & '.join(map(str, table_copy.colnames)) + line_ending
        for row in zip(*table_copy.columns):
            result += ' & '.join(map(str, row)) + line_ending
        result += r'\end{tabular}'

        return result

    def write_latex(self, filepath, show_row_numbers=False):
        """Write given table to file in LaTeX tabular format"""
        if not filepath.endswith('.tex'):
            raise ValueError('Filepath extension is not ".tex".')
        with open(filepath, 'x') as file:
            file.write(self.to_latex(show_row_numbers=show_row_numbers))

    @classmethod
    def from_csv(cls, filepath, comment_char='#'):
        """Read csv file and return a Table instance made of it

        If the first line in the csv file contains letters, it is
        assumed to be a header row and used for colnames.

        Lines starting with the comment_char are ignored.
        """
        with open(filepath) as file:
            rows = []
            colnames = []

            for line in file:
                line = line.strip()
                if not line or line[0] == comment_char:
                    continue

                if not rows and any(char.isalpha() for char in line):
                    colnames = line.split(',')
                else:
                    rows.append(list(map(float, line.split(','))))

            return cls(*zip(*rows), colnames=colnames)


def read_csv(filepath, comment_char='#'):
    """Read a csv file and return a Table instance made of it

    If the first line in the csv file contains letters, it is assumed
    to be a header row and ignored.
    Lines starting with comment_char are ignored too.

    To assign the returned value, use unpacking:

        col1, col2, col3 = labtables.read_csv(filepath)

    To use numpy arrays instead of lists, map it over the returned:

        col1, col2, col3 = map(np.array, labtables.read_csv(filepath))

    """
    return Table.from_csv(filepath, comment_char=comment_char).columns


def convert_csv_to_latex(csv_filepath, latex_filepath):
    """Convert csv_filepath into LaTeX, and write to latex_filepath

    First line in the csv file counts, even if it contains letters.
    Lines starting with # are ignored.
    """
    Table.from_csv(csv_filepath).write_latex(latex_filepath)


def test():
    from os import makedirs
    test_dir = 'test_tables/'
    makedirs(test_dir, exist_ok=True)

    a, b, c = ((i, i + 1, i + 2) for i in [1, 5, 10])
    print(f'a = {a}\nb = {b}\nc = {c}')
    table = Table(a, b, c, colnames=['a', 'b', 'c'])

    print(table, table.add_row_numbers(), table.to_csv(show_row_numbers=True),
          table.to_latex(), sep='\n\n')

    table.write_csv(test_dir + 'labtable-example-1.csv')
    table.write_csv(test_dir + 'labtable-example-2.csv', show_row_numbers=True)
    table.write_latex(test_dir + 'labtable-example-1.tex')
    table.write_latex(test_dir + 'labtable-example-2.tex', show_row_numbers=True)

    a_, b_, c_ = Table.from_csv(test_dir + 'labtable-example-1.csv').columns
    assert a_ == a and b_ == b and c_ == c

    a_, b_, c_ = read_csv(test_dir + 'labtable-example-1.csv')
    assert a_ == a and b_ == b and c_ == c


if __name__ == '__main__':
    test()
