from dataclasses import dataclass
from pathlib import Path
from typing import final, Sequence, Self, Dict

import pandas as pd

from magn.database.sqlite3 import SQLite3DataReader, SQLite3KeysReader, get_table_names
from magn.database.keys import Keys
from magn.database.topological_sort import TopologicalSorter


@final
@dataclass(slots=True)
class Database:
    """Holds the data and keys of the database tables."""

    # (Table name) => (Table data)
    tables: Dict[str, pd.DataFrame]
    # (Table name) => (Table keys data)
    keys: Dict[str, Keys]

    def __post_init__(self) -> None:
        if len(self.tables) != len(self.keys):
            raise ValueError(f"Number of tables and keys do not match ({len(self.tables)} vs {len(self.keys)}).")

    @classmethod
    def from_sqlite3(cls, file: Path) -> Self:
        """Substitute for the lack in the ability to create many constructors in python.
        Creates a Database object from an SQLite3 database file."""

        all_tables = get_table_names(file)

        keys_reader = SQLite3KeysReader(file, all_tables)
        keys = keys_reader.read()

        data_reader = SQLite3DataReader(file, all_tables, keys)
        data = data_reader.read()

        return cls(data, keys)

    def get_dependency_graph(self) -> Dict[str, Sequence[str]]:
        """Returns the dependency graph of the database."""

        return {table: list(self.keys[table].foreign_keys.keys()) for table in self.keys}

    def sort(self) -> Sequence[str]:
        """Sorts the tables in the database topologically."""

        dependencies = self.get_dependency_graph()
        sorter = TopologicalSorter()

        return list(reversed(list(sorter.sort(dependencies))))