import os


class Context:
    def __init__(self, fp: str, is_name: bool = False) -> None:
        """context class to hold code information"""
        if is_name:
            self.fp = self.fn = fp
            self.fd = None
        else:
            self.fp = os.path.abspath(fp)  # file path
            self.fn = os.path.basename(self.fp)  # file name
            self.fd = os.path.dirname(self.fp)  # file dir
