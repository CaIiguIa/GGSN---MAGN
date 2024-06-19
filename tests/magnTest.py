import random
from pathlib import Path
from typing import Final

import pandas as pd

from magn.database.database import Database
from magn.database.mock_database import mock_database
from magn.magn import MAGNGraph
from magn.prediction_type import PredictionType

resources_dir: Final[Path] = Path('../resources/data/')
zip_data_file: Final[Path] = resources_dir.joinpath('pitchfork-data.zip')
database_path: Final[Path] = resources_dir.joinpath('database.sqlite')

# database = Database.from_sqlite3(database_path)
database = mock_database()

magn = MAGNGraph.from_database(database)

x_train = database.create_mock_target('reviews', seed_id=random.randint(0, 1000))
magn.fit(x_train, 10000, 0.1)

x_test = x_train.iloc[2]
x_test = pd.Series(x_test)
x_test.drop("target", inplace=True)
print(x_test)
print(x_test.keys())
prediction = magn.predict(x_test, 'score', prediction_type=PredictionType.REGRESSION)
print(f"Predicted score: {prediction}, should be {x_test['score']}")

# TODO: wszędzie mamy założenie, że dane kategoryczne są w postaci stringów, ale to nie zawsze jest prawda
# id tabeli to są przecież categoricale - nie będą interpolowane jak dane regresyjne
# przykładowy fix to wczytywanie ich jako stringi, ale potrzeba informacji o typach kolumn
