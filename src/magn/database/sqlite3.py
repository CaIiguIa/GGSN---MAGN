import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, final, List, Dict

import pandas as pd

from magn.database.keys import Keys


def get_table_names(file: Path) -> List[str]:
    """Retrieve the names of all tables in the database."""

    with sqlite3.connect(file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT
                    name
                FROM
                    sqlite_master
                WHERE
                    type='table';
            """)

        tables = cursor.fetchall()
        table_names = list(table[0] for table in tables)

    return table_names


@final
@dataclass(slots=True)
class SQLite3KeysReader:
    """Reads the primary and foreign keys of the given tables in the SQLite3 database."""
    file: Path
    columns: List[str]

    def read(self) -> Dict[str, Keys]:
        found_keys: Dict[str, Keys] = {}

        for table in self.columns:
            primary_keys = self._get_primary_keys(table)
            foreign_keys = self._get_foreign_keys(table)

            found_keys[table] = Keys(primary_keys, foreign_keys)

        return found_keys

    def _get_primary_keys(self, table: str) -> List[str]:
        with sqlite3.connect(self.file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                PRAGMA
                    table_info({table});
            """)

            primary_keys: List[str] = []

            for column in cursor.fetchall():
                if column[5] == 1:
                    primary_keys.append(column[1])

            return primary_keys

    def _get_foreign_keys(self, table: str) -> Dict[str, Tuple[str, str]]:
        with sqlite3.connect(self.file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                PRAGMA
                    foreign_key_list({table});
            """)

            foreign_keys: Dict[str, Tuple[str, str]] = {}

            for column in cursor.fetchall():
                foreign_keys[column[2]] = (column[3], column[4])

            return foreign_keys


@final
@dataclass(slots=True)
class SQLite3DataReader:
    file: Path
    columns: List[str]
    keys: Dict[str, Keys]

    def read(self) -> Dict[str, pd.DataFrame]:
        dataframes: Dict[str, pd.DataFrame] = {}

        with sqlite3.connect(self.file) as conn:
            for index, table in enumerate(get_table_names(self.file)):
                query: str = f"""
                    SELECT
                        *
                    FROM
                        {table};
                """

                keys = self.keys[table]

                data = pd.read_sql_query(query, conn)
                data.set_index(
                    list({*keys.primary_keys, *list(map(lambda x: x[0], keys.foreign_keys.values()))}),
                    inplace=True,
                )
                data.name = table

                dataframes[table] = data

        return dataframes
