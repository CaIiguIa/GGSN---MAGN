from pathlib import Path
from typing import Final

import pandas as pd

from magn.database.database import Database
from magn.magn import MAGNGraph

resources_dir: Final[Path] = Path('../resources/data/')
zip_data_file: Final[Path] = resources_dir.joinpath('pitchfork-data.zip')
database_path: Final[Path] = resources_dir.joinpath('database.sqlite')

magn = MAGNGraph.from_sqlite3(database_path)

database = Database.from_sqlite3(database_path)

x_train = database.create_mock_target('reviews')
magn.fit(x_train, 10, 0.1)

x_test = x_train.iloc[0]
x_test = pd.Series(x_test)
x_test['target'] = 'score'
prediction = magn.predict(x_test, 'score')
print(f"Predicted score: {prediction}, should be {x_test['score']}")

# TODO: wszędzie mamy założenie, że dane kategoryczne są w postaci stringów, ale to nie zawsze jest prawda
# id tabeli to będą categoricale
# przykładowy fix to wczytywanie ich jako stringi, ale potrzeba informacji o typach kolumn
