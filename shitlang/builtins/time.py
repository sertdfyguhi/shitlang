import time


class TimeBuiltins:
    def sleep(self, seconds: int | float):
        time.sleep(seconds)

    def now(self):
        return time.time()
