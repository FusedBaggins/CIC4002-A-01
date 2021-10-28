import io
import re
from time import sleep


class IndexGenerator:
    def __init__(self):
        self.__indexes_path__ = '../files/'
        self.lineSize = None
        self.lastLine = None
        self.lines = None
        self.hashIndexes = {}

    def get_initial_line_position(self, file):
        file.seek(0)
        self.lineSize = len(file.readline())
        self.lastLine = file.seek(0, io.SEEK_END) - self.lineSize
        self.lines = int(self.lastLine / self.lineSize)

    def append_hash_index(self, _hash, position):
        pass

    def sequential_index(self, field=0):
        with open(f'{self.__indexes_path__}serialized.bin', 'rb') as file:
            with open(f'{self.__indexes_path__}SI0{field}.bin', 'ab') as index_file:
                self.get_initial_line_position(file)
                curr = 0
                while curr <= self.lastLine:
                    file.seek(curr, 0)
                    line = re.compile(r'(\+)+').split(file.readline().decode('latin-1'))[-1]

                    split_line = line.split(';')
                    self.set_hash_index(split_line[2], curr)
                    index_file.write(bytes(f'{split_line[field]},{curr}\n', 'latin-1'))
                    curr += self.lineSize

        print(f'Sequential indexes of {field} was been successful created')

    def set_hash_index(self, key, position):
        try:
            self.hashIndexes[hash(key)].append(position)
        except KeyError:
            self.hashIndexes[hash(key)] = [position]


if __name__ == '__main__':
    ig = IndexGenerator()
    ig.sequential_index()
    print(ig.hashIndexes)
