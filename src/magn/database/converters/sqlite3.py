import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, final

from magn.asa.ASAGraph import ASAGraph
from magn.database.converters.interface import Converter
from magn.magn import MAGNGraph


@final
@dataclass(slots=True)
class SQLite3Converter(Converter):
    file: Path

    def __post_init__(self) -> None:
        pass

    def convert(self) -> MAGNGraph:
        graph = MAGNGraph()
        tables = self._get_all_table_names()

        for table in tables:
            columns = self._get_columns(table)


        raise NotImplementedError()

    def _get_all_table_names(self) -> Tuple[str, ...]:
        with sqlite3.connect(self.file) as conn:
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
            table_names = tuple(table[0] for table in tables)

        return table_names

    def _get_columns(self, table: str) -> Tuple[str, ...]:
        with sqlite3.connect(self.file) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                PRAGMA
                    table_info({table});
            """)
            columns = cursor.fetchall()
            column_names = tuple(column[1] for column in columns)

        return column_names
