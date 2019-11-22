from abc import ABCMeta, abstractmethod


class Drawable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw(self, screen): raise NotImplementedError
