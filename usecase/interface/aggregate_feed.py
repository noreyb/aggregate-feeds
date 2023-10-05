import abc


class IAggregateFeed(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError
