from dataclasses import dataclass
import os


@dataclass
class Position:
    ln: int = 1
    col: int = 0
    i: int = -1

    def __str__(self):
        return f"line {self.ln} at char {self.col}"


class Context:
    def __init__(
        self,
        fp: str,
        is_name: bool = False,
        pos: Position = Position(),
        end_pos: Position | None = None,
    ) -> None:
        """context class to hold code information"""
        if is_name:
            self.fp = self.fn = fp
            self.fd = None
        else:
            self.fp = os.path.abspath(fp)  # file path
            self.fn = os.path.basename(self.fp)  # file name
            self.fd = os.path.dirname(self.fp)  # file dir

        self.pos = pos
        self.end_pos = end_pos

    def __repr__(self) -> str:
        return f"Context(fn={self.fn})"
