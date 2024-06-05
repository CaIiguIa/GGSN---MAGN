import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, final, List, Sequence

import pandas as pd

from magn.database.converters.interface import Converter
from magn.database.database import Database
from magn.database.structures.graph import Graph


@final
@dataclass(slots=True)
class SQLite3Converter(Converter):
    file: Path

    def __post_init__(self) -> None:
        pass

    def convert(self) -> Database:
        tables = self._get_all_table_names()
        tables_dataframe: List[pd.DataFrame] = []
        graph: Graph[int] = Graph()

        with sqlite3.connect(self.file) as conn:
            for index, table in enumerate(tables):
                query: str = f"""
                    SELECT
                        *
                    FROM
                        {table};
                """

                tables_dataframe.append(
                    pd.DataFrame(
                        pd.read_sql_query(query, conn),
                        columns=self._get_all_columns(table),
                    )
                )

                foreign_keys_query: str = f"""
                    PRAGMA
                        foreign_key_list({table});
                """
                # foreign_keys = pd.read_sql_query(foreign_keys_query, conn)
                # for foreign_key in foreign_keys:
                #     graph.add_edge(index, tables.index(foreign_key['table']))



        return Database(tables_dataframe, graph)

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

    def _get_all_columns(self, table: str) -> List[str]:

        column_name_column: int = 1
        with sqlite3.connect(self.file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                PRAGMA
                    table_info({table});
            """)

            columns = cursor.fetchall()
            column_names = list(column[column_name_column] for column in columns)

        return column_names
