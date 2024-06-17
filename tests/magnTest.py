from pathlib import Path
from typing import Final

from magn.database.database import Database
from magn.magn import MAGNGraph

resources_dir: Final[Path] = Path('../resources/data/')
zip_data_file: Final[Path] = resources_dir.joinpath('pitchfork-data.zip')
database_path: Final[Path] = resources_dir.joinpath('database.sqlite')

magn = MAGNGraph.from_sqlite3(database_path)

database = Database.from_sqlite3(database_path)

x_train = database.create_mock_target('reviews')
magn.fit(x_train, 10, 0.1)
