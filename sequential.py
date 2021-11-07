import gc
import io
import re
from pathlib import Path


class Sequential:
    def __init__(self, file, line_size, bucket_size=5, allow_create=False):
        self.bucket_size = bucket_size
        self.index_line = 0

        if not line_size:
            file.seek(0, 0)
            lines = file.readlines()
            line_size = len(max(lines, key=len))

            # Free memory
            del lines
            gc.collect()

        if not self.index_line and not allow_create:
            with open('./files/index_01.bin', 'rb') as index_file:
                file.seek(0, 0)
                lines = index_file.readlines()
                self.index_line = len(max(lines, key=len))

                # Free memory
                del lines
                gc.collect()

        if allow_create:
            self.create(file, line_size)

    @staticmethod
    def __serialize_line__(line):
        return re.compile(r'(\+)+').split(line.decode('latin-1'))[-1]

    @staticmethod
    def __read_byte__(file):
        c = ''
        while byte := file.read(1):
            b = byte.decode('latin-1')
            if b == ' ':
                break
            elif b != '+' and b != ' ':
                c += b
        c = c.split("-")
        return [int(number) for number in c]

    def __linear_search__(self, line, code):
        positions = [int(number) for number in line.split(' ')[1:]]

        with open('./files/data.bin', 'rb') as file:
            find = False
            for position in positions:
                file.seek(position, 0)
                values = self.__serialize_line__(file.readline()).replace('\n', '').split(';')

                if int(values[0]) == code:
                    find = True
                    print("\nFound it!")
                    print(
                        '{',
                        f'id: {values[0]}, Living Place: {values[1]}, Gender: {values[3]}, Age: {values[4]}, Years coding: {values[2]}',
                        '}')
                    break

            if not find:
                print(f'None register found with code {code}. :(')

    def create(self, file, line_size):
        curr = 0
        eof = file.seek(0, io.SEEK_END) - line_size

        positions = []
        first = None
        with open('./files/temp.bin', 'xb+') as temp:
            while curr <= eof:
                file.seek(curr, 0)
                line = self.__serialize_line__(file.readline())
                code = line.split(';', 1)[0]
                length = len(positions)
                if length < self.bucket_size:
                    if not length:
                        first = code
                    positions.append(str(curr))
                else:
                    merged = " ".join(positions)
                    merged = f'{first}-{code} {merged}\n'
                    temp.write(bytes(merged, 'latin-1'))

                    positions = [str(curr)]
                    first = code

                curr += line_size

            with open('./files/index_01.bin', 'wb') as index_f:
                temp.seek(0, 0)
                lines = temp.readlines()
                self.index_line = len(max(lines, key=len))

                for line in lines:
                    line = line.decode('latin-1')
                    index_f.write(bytes(f'{line:{"+"}{">"}{self.index_line}}', 'latin-1'))

        # Remove temp file
        Path('./files/temp.bin').unlink()

    def search(self, code):
        with open('./files/index_01.bin', 'rb') as index_f:
            low = mid = 0
            find = False
            high = index_f.seek(0, io.SEEK_END) // self.index_line

            while low <= high:

                mid = ((high + low) // 2)
                index_f.seek(mid * self.index_line, 0)
                range_codes = self.__read_byte__(index_f)

                # reset cursor
                index_f.seek(mid * self.index_line, 0)

                if range_codes[0] < code < range_codes[1]:
                    find = True
                    self.__linear_search__(self.__serialize_line__(index_f.readline()).replace('\n', ''), code)
                    break

                if range_codes[0] < code:
                    low = mid + 1

                elif range_codes[0] > code:
                    high = mid - 1

                else:
                    find = True
                    self.__linear_search__(self.__serialize_line__(index_f.readline()).replace('\n', ''), code)
                    break

            if not find:
                print(f"I can't find any register with code {code}")
