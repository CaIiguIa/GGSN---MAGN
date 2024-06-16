"""Contains the Keys class, which represents a set of keys for a table."""

from dataclasses import dataclass
from typing import final, List, Dict, Tuple


@final
@dataclass(slots=True)
class Keys:
    """Represents a set of keys for a table."""

    # List of primary keys (column names)
    primary_keys: List[str]

    # Dictionary of foreign keys - (what other table) => (from column, to column)
    foreign_keys: Dict[str, Tuple[str, str]]
