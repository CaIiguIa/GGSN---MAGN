from pathlib import Path
from typing import Final
from magn.magn import MAGNGraph

resources_dir: Final[Path] = Path('resources/data/')
zip_data_file: Final[Path] = resources_dir.joinpath('pitchfork-data.zip')
database_path: Final[Path] = resources_dir.joinpath('database.sqlite')

MAGNGraph.from_sqlite3(Path(r"C:\Users\sdjur\programowanie\pycharm\GGSN---MAGN\resources\data\database.sqlite"))
