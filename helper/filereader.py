import os
class Filereader:
    def __init__(self):
        self.__cwd = os.path.dirname(__file__)
        self.__raw_lines = []

    @property
    def cwd(self): return self.__cwd
    @property
    def rel_path(self): return self.__rel_path
    @property
    def raw_lines(self): return self.__raw_lines

    @raw_lines.setter
    def raw_lines(self, value):
        self.__raw_lines = value

    def read(self, filepath = None):
        if not filepath: return
        rel_path =  os.path.abspath(os.path.join(self.cwd, "..", "views", filepath))
        if not os.path.exists(rel_path): raise Exception(f"File not found: {rel_path}")
        with open(rel_path) as f:
            self.raw_lines = f.readlines()
        return self

    def encode(self):
        return "".join(line.rstrip("\n").strip() for line in self.raw_lines)
