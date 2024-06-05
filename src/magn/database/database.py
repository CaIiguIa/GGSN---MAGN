from dataclasses import dataclass
from typing import final, Sequence

import pandas as pd

from magn.database.structures.graph import Graph


@final
@dataclass(slots=True)
class Database:
    tables: Sequence[pd.DataFrame]
    graph: Graph[int]

    def __post_init__(self) -> None:
        if len(self.tables) != len(self.graph)[0]:
            raise ValueError(f"""
            The number of tables and the number of vertices in the graph must be equal. 
            Tables: {len(self.tables)}, Vertices: {len(self.graph)}
            """)

