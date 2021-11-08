import gc
import io
import re


class Node:
    def __init__(self, key, position):
        self.left = None
        self.right = None
        self.key = key
        self.positions = [position]

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

    def set_max_node(self, btree):
        if not btree.max_node:
            btree.max_node = (self.key, len(self.positions))

        condition = len(self.positions) > btree.max_node[1]
        btree.max_node = (self.key, len(self.positions)) if condition else btree.max_node

        if self.left:
            self.left.set_max_node(btree)
        if self.right:
            self.right.set_max_node(btree)

    def insert(self, key, position):
        if self.key:
            if key < self.key:
                if self.left is None:
                    self.left = Node(key, position)
                else:
                    self.left.insert(key, position)
            elif key > self.key:
                if self.right is None:
                    self.right = Node(key, position)
                else:
                    self.right.insert(key, position)
            elif key == self.key:
                self.positions.append(position)
        else:
            self.key = key
            self.positions = [position]

    def search(self, key, analytics=False):
        if self.key == key:
            if not analytics:
                print(f"WOW!!! I found {len(self.positions)} register with this key.")
                input("I'll show only 500 lines, ok? Press enter to print the lines.\n")

                with open('./files/data.bin', 'rb') as file:
                    for position in self.positions:
                        file.seek(position, 0)
                        self.__print_line__(file.readline())
            else:
                print(len(self.positions))
        else:
            if self.left:
                self.left.search(key, analytics)
            if self.right:
                self.right.search(key, analytics)


class BTree:
    def __init__(self, file, line_size):
        self.values = None
        self.max_node = None

        if not line_size:
            file.seek(0, 0)
            lines = file.readlines()
            line_size = len(max(lines, key=len))

            # Free memory
            del lines
            gc.collect()

        self.create(file, line_size)

    @staticmethod
    def __serialize_line__(line):
        return re.compile(r'(\+)+').split(line.decode('latin-1'))[-1]

    def create(self, file, line_size):
        curr = 0
        eof = file.seek(0, io.SEEK_END) - line_size

        while curr <= eof:
            file.seek(curr, 0)
            line = self.__serialize_line__(file.readline())
            values = line.split(';')

            if self.values:
                self.values.insert(values[1], curr)
            else:
                self.values = Node(values[1], curr)

            curr += line_size
