from abc import ABC
import math
from V2.Problem.AbstractProblem import Problem


class PrimalityTest(Problem, ABC):
    def __init__(self):
        super().__init__()

    def run(self, setMin, setMax):
        for num in range(setMin, setMax):
            if isPrime(num):
                self.res.append(num)


def isPrime(test):
    if test < 2:
        return False
    for i in range(2, 1 + math.floor(math.sqrt(test))):
        if test % i == 0:
            return False
    return True

