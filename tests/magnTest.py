from pathlib import Path
from typing import Final
from magn.magn import MAGNGraph

resources_dir: Final[Path] = Path('../resources/data/')
zip_data_file: Final[Path] = resources_dir.joinpath('movie-data-analytics-dataset.zip')
database_path: Final[Path]  = resources_dir.joinpath('movie.sqlite')

MAGNGraph.from_sqlite3(database_path)
