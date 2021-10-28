import pandas as pd

__file_path__ = '../files/'


def __fill_lines__():
    with open(f'{__file_path__}serialized.csv', 'r') as file:
        lines = file.readlines()
        max_line_length = len(max(lines, key=len))
        with open(f'{__file_path__}serialized.bin', 'ab+') as bin_file:
            for line in lines:
                bin_file.write(bytes(f'{line:{"+"}{">"}{max_line_length}}', 'UTF-8'))


def serialize_file():
    # Respondent,Country,YearsCoding,Gender,Age
    df = pd.read_csv(
        filepath_or_buffer=f'{__file_path__}initial.csv',
        sep=',',
        dtype=str,
        engine='c',
        usecols=['Respondent', 'Country', 'Age', 'Gender', 'YearsCoding'],
        encoding='latin-1'

    )

    df = df.fillna('None')
    df.loc[(df.Gender.str.contains(';') & ~df.Gender.isna()), 'Gender'] = 'Other'
    df.loc[(df.Gender.str.contains(',') & ~df.Gender.isna()), 'Gender'] = 'Other'
    df.to_csv(path_or_buf=f'{__file_path__}serialized.csv', sep=';', index=False, header=False, encoding='latin-1')

    # Create a .bin file with fixed line size
    __fill_lines__()


if __name__ == '__main__':
    serialize_file()
