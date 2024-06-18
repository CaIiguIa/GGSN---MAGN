"""Contains the Keys class, which represents a set of keys for a table."""

from dataclasses import dataclass, astuple
from typing import final, List, Dict, Tuple, Iterator


@final
@dataclass(slots=True)
class Keys:
    """Represents a set of keys for a table."""

    # List of primary keys (column names)
    primary_keys: List[str]

    # Dictionary of foreign keys - (what other table) => (from column, to column)
    foreign_keys: Dict[str, Tuple[str, str]]

    def __iter__(self) -> Iterator:
        """Returns an iterator over the dataclass fields. Basically lets you unpack all the fields of the dataclass."""
        return iter(astuple(self))
