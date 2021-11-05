import gc
import io
import re


class Hash:
    def __init__(self, file, line_size):
        self.values = {}
        self.analytics = {}

        if not line_size:
            file.seek(0, 0)
            lines = file.readlines()
            line_size = len(max(lines, key=len))

            # Free memory
            del lines
            gc.collect()

        self.create(file, line_size)

    @staticmethod
    def __create_hash__(value):
        if not value == 'None':
            values = re.findall(r'[0-9]+', value)
            key = 0
            for v in values:
                key += int(v)
            return hash(key)
        return hash(0)

    @staticmethod
    def __serialize_line__(line):
        return re.compile(r'(\+)+').split(line.decode('latin-1'))[-1]

    def __print_line__(self, line):
        line = self.__serialize_line__(line)
        values = line.split(';')

        print(
            '{',
            f'id: {values[0]}, Living Place: {values[1]}, Gender: {values[3]}, Age: {values[4]}, Years coding: {values[2]}',
            '}')

    def __analytics__(self, keys):
        for obj in keys:
            self.analytics[obj['hash']] = {'items': len(self.values[obj['hash']]), 'key': obj['key']}

    def create(self, file, line_size):
        curr = 0
        keys = []
        eof = file.seek(0, io.SEEK_END) - line_size

        while curr <= eof:
            file.seek(curr, 0)
            line = self.__serialize_line__(file.readline())
            values = line.split(';')
            key = self.__create_hash__(values[2])
            keys.append({'hash': key, 'key': values[2]})

            try:
                self.values[key].append(curr)
            except KeyError:
                self.values[key] = [curr]

            curr += line_size
        self.__analytics__(keys)

    def search(self, file_path, value):
        try:
            key = self.__create_hash__(value)
            print(key)
            print(f"WOW!!! I found {len(self.values[key])} register with this key.")
            input("I'll show only 500 lines, ok? Press enter to print the lines.\n")

            with open(file_path, 'rb') as file:
                for i in range(0, 500, 1):
                    file.seek(self.values[key][i], 0)
                    self.__print_line__(file.readline())

            print(self.analytics)
        except KeyError:
            print("Sorry 'bout that. Your key does not exist on index.")

    def print_analytics(self):
        items = 0
        for obj in self.analytics.values():
            items += obj['items']

        for obj in self.analytics.items():
            print(f"{obj[1]['key']}: ~{(obj[1]['items'] * 100) // items}%")
