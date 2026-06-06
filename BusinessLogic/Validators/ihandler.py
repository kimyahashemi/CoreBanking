from abc import abstractmethod, ABC


class IHandler(ABC):
    @abstractmethod
    def set_next(self, next_handler):
        pass

    @abstractmethod
    def validate(self, request):
        pass
