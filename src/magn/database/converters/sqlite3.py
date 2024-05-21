import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, final

from magn.asa.ASAGraph import ASAGraph
from magn.database.converters.interface import Converter
from magn.mang import MAGNGraph


@final
@dataclass(slots=True)
class SQLite3Converter(Converter):
    file: Path

    def __post_init__(self) -> None:
        pass

    def convert(self) -> MAGNGraph:
        graph = MAGNGraph()

        with sqlite3.connect(self.file) as connection:
            pass

    def get_all_table_names(self) -> Tuple[str, ...]:
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

    def fetch_individual_table(self, table_name: str) -> ASAGraph:
        pass
