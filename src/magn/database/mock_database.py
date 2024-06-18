import pandas as pd

from magn.database.database import Database
from magn.database.keys import Keys


def mock_database() -> Database:
    reviews = mock_reviews()
    years = mock_years()
    labels = mock_labels()
    genres = mock_genres()
    content = mock_content()
    artists = mock_artists()

    return Database(
        tables={
            'reviews': reviews,
            'years': years,
            'labels': labels,
            'genres': genres,
            'content': content,
            'artists': artists,
        },
        keys={
            'reviews': Keys(primary_keys=['reviewId'], foreign_keys={}),
            'years': Keys(primary_keys=[], foreign_keys={'reviews': ('reviewId', 'reviewId')}),
            'labels': Keys(primary_keys=[], foreign_keys={'reviews': ('reviewId', 'reviewId')}),
            'genres': Keys(primary_keys=[], foreign_keys={'reviews': ('reviewId', 'reviewId')}),
            'content': Keys(primary_keys=[], foreign_keys={'reviews': ('reviewId', 'reviewId')}),
            'artists': Keys(primary_keys=[], foreign_keys={'reviews': ('reviewId', 'reviewId')}),
        }
    )


def mock_reviews() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'title': ['Album 1', 'Album 2', 'Album 3', 'Album 4', 'Album 5'],
            'score': [1.5, 3.0, 7.5, 9.0, 5.5],
            'author': ['aberfeldy', 'aarktica', 'aberdeen', 'aceyalone', 'aceyalone'],
            'author_type': ['senior staff writer', 'contrinutor', 'senior staff writer', 'contributor',
                            'senior staff writer'],
            'pub_date': ['2020-01-01', '2021-01-02', '2022-01-03', '2020-01-04', '2022-01-05'],
            'genre': ['rock', 'pop', 'rap', 'rock', 'pop'],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )


def mock_years() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'year': [2020, 2021, 2022, 2020, 2022],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )


def mock_labels() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'label': ['rough trade', 'silber', 'better looking', 'deconstruction', 'silber'],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )


def mock_genres() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'genre': ['rock', 'pop', 'experimental', 'rock', 'electronic'],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )


def mock_content() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'content': [
                'Aberfeldy recorded their debut, Young Forever, using a single microphone.',
                'Can there be any purpose behind a masters degree in the psychology of music other than attempting',
                'If you caught this little blip in the mid-90s, you must have had a pretty sensitive radar.',
                'Brad: Welcome to our wrap-up of Game Four between the East Coast and West Coast Hip-Hop Finals',
                'Aceyalones transcendent smoothness is such that he can reference Laverne and Shirley'
            ],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )


def mock_artists() -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'artist': ['Aberfeldy', 'aarktica', 'aberdeen', 'aceyalone', 'aceyalone'],
        },
        index=pd.Index([0, 1, 2, 3, 4], name='reviewId')
    )
