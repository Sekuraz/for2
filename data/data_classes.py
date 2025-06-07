import enum
import textwrap

import numpy as np

from .enum_helper import with_limits

dtype = np.uint8

@with_limits
class Opening(enum.Flag):
    RIGHT = enum.auto()
    LEFT = enum.auto()
    TOP = enum.auto()
    BOTTOM = enum.auto()

    def __int__(self):
        return self.value

    def __float__(self):
        return self.value / (Opening.ALL.value + 1)


class Openings:
    def __init__(self, size, borders=None, np_array=None, position=None):
        self.size = size
        self.openings: list[Opening] = [Opening.NONE for _ in range(size * size)]

        if borders:
            self.parse_borders(borders)
        if np_array is not None:
            self._parse_np(np_array)

        self.position = position
        if position is not None:
            self.position = np.array(position * size, dtype=np.int32)

    def _parse_np(self, np_array: np.ndarray):
        if np_array.dtype == np.uint8:
            self.openings = [Opening(int(value)) for value in np_array]
        elif np_array.dtype == np.float32:
            self.openings = [Opening(int(round(value * (Opening.ALL.value + 1), 0))) for value in np_array]

    def parse_borders(self, borders):
        x = 0
        y = 0
        for chunk in textwrap.wrap(borders, 2):
            if chunk[0] == "r":
                self[(x, y)] |= Opening.RIGHT
                self[(x + 1, y)] |= Opening.LEFT
            if chunk[1] == "b":
                self[(x, y)] |= Opening.BOTTOM
                self[(x, y + 1)] |= Opening.TOP

            x += 1
            if x == self.size:
                x = 0
                y += 1

    def __getitem__(self, item) -> Opening:
        x, y = item
        return self.openings[int(y) * self.size + int(x)]

    def __setitem__(self, key, value: Opening):
        x, y = key
        self.openings[y * self.size + x] = value

    def __str__(self):
        ret = "┌" + "-" * (3 * self.size - 1) + "┐\n"
        for y in range(self.size):
            cell_row = "|"
            border_row = "|" if y < self.size - 1 else "└"
            for x in range(self.size):
                if self.position is not None and self.position[0] == x and self.position[1] == y:
                    cell_row += "XX"
                else:
                    cell_row += "  "  # the cell is empty
                cell_row += " " if self[x, y] & Opening.RIGHT else "|"
                border_row += "  " if self[x, y] & Opening.BOTTOM else "--"
                border_row += "┼" if y < self.size - 1 else "-"
            ret += cell_row + "\n"
            ret += border_row + "\n"
        ret = ret[:-2] + "┘"
        return ret

    def to_np_array(self, typ=None):
        if typ is None:
            typ = dtype
        return np.array(self.openings, dtype=typ)

    def to_np_array_binary(self, typ=None):
        if typ is None:
            typ = dtype
        res = [1] * (self.size * 2 + 1)
        for y in range(self.size):
            cell_row = [1]
            border_row = [1]
            for x in range(self.size):
                cell_row.append(0)
                cell_row.append(0 if self[x, y] & Opening.RIGHT else 1)
                border_row.append(0 if self[x, y] & Opening.BOTTOM else 1)
                border_row.append(1)
            res.extend(cell_row)
            res.extend(border_row)
        return np.array(res, dtype=typ)

class Path:
    def __init__(self, size, string_path=None, np_path=None):
        assert string_path is not None or np_path is not None

        self.size = size
        self.length: int = 0
        self.string = None
        self.path: list[Opening] = [Opening.NONE for _ in range(size * size)]
        self.map = {0: Opening.NONE, Opening.NONE: 0, 1: Opening.RIGHT, Opening.RIGHT: 1, 2: Opening.LEFT,
                    Opening.LEFT: 2, 3: Opening.TOP, Opening.TOP: 3, 4: Opening.BOTTOM, Opening.BOTTOM: 4}


        if string_path:
            self.parse_string(string_path)
        if np_path is not None:
            self.parse_np(np_path)

    def __iter__(self):
        for element in self.path:
            if element is not Opening.NONE:
                yield element
            else:
                return

    def parse_np(self, np_path: np.ndarray):
        if np_path.dtype == np.uint8:
            self.path = [Opening(value) for value in np_path]
        elif np_path.dtype == np.float32:
            np_path *= 4
            np_path.round(0)
            self.path = [self.map[int(value)] for value in np_path]
        else:
            raise NotImplementedError


    def parse_string(self, path):
        for i, s in enumerate(path):
            if s == "r":
                self.path[i] = Opening.RIGHT
            elif s == "l":
                self.path[i] = Opening.LEFT
            elif s == "t":
                self.path[i] = Opening.TOP
            elif s == "b":
                self.path[i] = Opening.BOTTOM

        self.length = i
        assert path == str(self)


    def __str__(self):
        map = {Opening.NONE: "", Opening.RIGHT: "r", Opening.LEFT: "l", Opening.TOP: "t", Opening.BOTTOM: "b"}
        return "".join(map[elem] for elem in self.path)

    def to_np_array(self, typ=None):
        if typ is None:
            typ = dtype
        if typ in (np.int8, np.uint8):
            return np.array(self.path, dtype=typ)
        elif typ == np.float32:
            map = {Opening.NONE: 0, Opening.RIGHT: 0.25, Opening.LEFT: 0.5, Opening.TOP: 0.75, Opening.BOTTOM: 1.0}
            target_values = [map[value] for value in self.path]
            return np.array(target_values, dtype=np.float32)
        else:
            raise NotImplementedError

class Maze:
    @classmethod
    def from_database(cls, width, borders, optimalPath, explorerMode, **kwargs):
        size = int(width)
        openings = Openings(size, borders)
        optimal_path = Path(size, string_path=optimalPath)
        ret = cls(size=size, openings=openings, optimal_path=optimal_path, explorer_mode=explorerMode)
        ret.verify()
        return ret

    def __init__(self, size, optimal_path, explorer_mode, openings):
        self.size = size
        self.openings: Openings = openings
        self.optimal_path = optimal_path
        self.explorer_mode = explorer_mode

    def __str__(self):
        return str(self.openings)

    def verify(self):
        pos = [0, 0]
        for step in self.optimal_path.path:
            assert self.openings[pos] & step == step, "impossible step"

            if self.openings[pos] & step != step:
                print("impossible step")

            if step == Opening.RIGHT:
                pos[0] += 1
            elif step == Opening.LEFT:
                pos[0] -= 1
            elif step == Opening.TOP:
                pos[1] -= 1
            elif step == Opening.BOTTOM:
                pos[1] += 1
