from abc import ABC, abstractmethod
from dataclasses import dataclass

from magn.magn import MAGNGraph


@dataclass(slots=True)
class Converter(ABC):

    @abstractmethod
    def convert(self) -> MAGNGraph:
        pass
