import abc

class Base():
    def __init__(self, clk):
        self._clk = clk

    @abc.abstractmethod
    def execute():
        pass
