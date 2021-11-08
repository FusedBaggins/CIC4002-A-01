import sys
from pathlib import Path

# third-party
import pandas as pd

from hash import Hash
from btree import BTree
from sequential import Sequential


def menu(file_handler):
    print("\n         MENU        ")
    print("1. Sequential Index")
    print("2. Sequential Index 2")
    print("3. Hash index")
    print("4. Btree index")
    print("5. Analytics")
    print("6. Exit")

    choice = int(input("\nYour option: "))

    if choice == 1:
        file_handler.sequential.search(int(input('Please, text id: ')))
        pass
    elif choice == 2:
        print("Ooops! There's nothing here. :D")
        pass
    elif choice == 3:
        file_handler.hash.search(f'{file_handler.file_path}data.bin')
        pass
    elif choice == 4:
        key = input("Please, text key: ")
        print(file_handler.btree.values.search(key, False))

    elif choice == 5:
        print("This section shows some questions about data.\n")
        print("1. How many brazilians answer the SO Survey?")
        file_handler.btree.values.search('Brazil', True)

        file_handler.btree.values.set_max_node(file_handler.btree)
        print("\n2. Which country answered the most to the survey?")
        print(f'Country: {file_handler.btree.max_node[0]} - {file_handler.btree.max_node[1]}')

    elif choice == 6:
        sys.exit(0)

    menu(file_handler)


class FileHandler:
    def __init__(self):
        self.file_path = './files/'
        self.encoding = 'latin-1'
        self.line_size = 0
        self.sequential = None

        if not Path(f'{self.file_path}/data.csv').exists():
            print("Oops, source file is missing (data.csv). Please download it from kaggle.")
            print("https://www.kaggle.com/stackoverflow/stack-overflow-2018-developer-survey")
            sys.exit(0)

        print("\nChecking if another files exist...")
        option = input("Do you wanna skip all files serializations? (y/n): ").lower()

        if option == 'n':
            print("That's fine. Now, I'm going to prepare source file.")
            for file in ['data.bin', 'index_01.bin', 'index_02.bin']:
                path = Path(f'{self.file_path}{file}')
                if path.exists():
                    path.unlink()
                with open(f'{self.file_path}{file}', 'xb'):
                    pass

            self.__write_bin_file__()
            with open(f'{self.file_path}data.bin', 'rb') as file:
                self.sequential = Sequential(file, self.line_size, allow_create=True)

            print("All serializations has completed. Now I need to create indexes.")

        with open(f'{self.file_path}data.bin', 'rb') as file:
            # self.file = file
            self.hash = Hash(file, self.line_size)
            self.btree = BTree(file, self.line_size)

            if not self.sequential:
                self.sequential = Sequential(file, self.line_size)

    def __write_bin_file__(self):
        df = pd.read_csv(
            filepath_or_buffer=f'{self.file_path}data.csv',
            sep=',',
            dtype=str,
            engine='c',
            usecols=['Respondent', 'Country', 'Age', 'Gender', 'YearsCoding'],
            encoding='latin-1'
        )

        df = df.fillna('None')
        df.loc[((df.Gender.str.contains(';') | df.Gender.str.contains(',')) & ~df.Gender.isna()), 'Gender'] = 'Other'
        df.to_csv(path_or_buf=f'{self.file_path}temp.csv', sep=';', index=False, header=False, encoding=self.encoding)

        with open(f'{self.file_path}temp.csv', 'r') as f:
            lines = f.readlines()
            self.line_size = len(max(lines, key=len))

            with open(f'{self.file_path}data.bin', 'wb') as file:
                for line in lines:
                    file.write(bytes(f'{line:{"+"}{">"}{self.line_size}}', self.encoding))

        Path(f'{self.file_path}temp.csv').unlink()


if __name__ == '__main__':
    fh = FileHandler()
    menu(fh)
