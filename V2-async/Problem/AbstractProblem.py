import abc


class Problem(abc.ABC):
    def __init__(self):
        self._res = list()

    @property
    def res(self):
        return self._res

    @abc.abstractmethod
    def run(self, setMin, setMax):
        pass
