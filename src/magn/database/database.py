"""Holds the Database class, which is a container for the data and keys of the database tables."""
from collections import defaultdict
from dataclasses import dataclass, astuple, field, InitVar
from pathlib import Path
from typing import final, Sequence, Self, Dict, List, Generator, Iterator, ClassVar, Optional
from random import seed, choice

import pandas as pd

from magn.database.sqlite3 import SQLite3DataReader, SQLite3KeysReader, get_table_names
from magn.database.keys import Keys
from magn.database.topological_sort import TopologicalSorter


@final
@dataclass(slots=True)
class Table:
    """Represents a table in the database."""
    data: pd.DataFrame
    keys: Keys

    def __iter__(self) -> Iterator:
        """Returns an iterator over the dataclass fields. Basically lets you unpack all the fields of the dataclass."""
        return iter(astuple(self))


@final
@dataclass(slots=True)
class Database:
    """Holds the data and keys of the database tables."""

    # (Table name) => (Table data, Table keys)
    all_data: Dict[str, Table] = field(init=False)

    # InitVar is used to prevent the fields from being initialized in the __init__ method.
    # They are not part of the object.
    tables: InitVar[Dict[str, pd.DataFrame]]
    keys: InitVar[Dict[str, Keys]]

    mock_column_name: ClassVar[str] = "target"

    def __post_init__(self, tables: Dict[str, pd.DataFrame], keys: Dict[str, Keys]) -> None:
        if len(tables) != len(keys):
            raise ValueError(f"Number of tables and keys do not match ({len(tables)} vs {len(keys)}).")

        if tables.keys() | keys.keys() != tables.keys() & keys.keys():
            raise ValueError("Keys in tables object do not match keys in keys object!")

        self.all_data = {table_name: Table(tables[table_name], keys[table_name]) for table_name in tables | keys}

    def __getitem__(self, item: str) -> Table:
        """Lets you subscript the Database object to get a Table object."""
        return self.all_data[item]

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

    def _get_dependency_graph(self) -> Dict[str, Sequence[str]]:
        """Returns the dependency graph of the database."""

        dependencies: Dict[str, List[str]] = defaultdict(list)

        for table_name, table in self.all_data.items():
            for foreign_table in table.keys.foreign_keys.keys():
                dependencies[foreign_table].append(table_name)
                dependencies[table_name]  # Ensure that the table is in the dictionary

        return dependencies

    def sort(self) -> Generator:
        """Sorts the tables in the database topologically."""

        dependencies = self._get_dependency_graph()
        sorter = TopologicalSorter()

        return sorter.sort(dependencies)

    def create_mock_target(self, table_name: str, choices_iterable: Optional[Sequence] = None, seed_id: int = 0
                           ) -> pd.DataFrame:
        """Creates a mock target DataFrame for the given table."""
        seed(seed_id)

        data, _ = self[table_name]
        if choices_iterable is None:
            choices_iterable = data.columns

        data[Database.mock_column_name] = data.apply(lambda _: choice(choices_iterable), axis=1)

        return data
