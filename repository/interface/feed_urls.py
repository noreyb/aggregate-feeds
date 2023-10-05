import abc


class IFeedURLs(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self) -> list:
        raise NotImplementedError
