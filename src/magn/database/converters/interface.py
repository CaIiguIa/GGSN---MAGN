from abc import ABC, abstractmethod
from dataclasses import dataclass

from magn.database.database import Database


@dataclass(slots=True)
class Converter(ABC):

    @abstractmethod
    def convert(self) -> Database:
        pass
