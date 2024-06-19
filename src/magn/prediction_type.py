from enum import Enum


class PredictionType(Enum):
    """Enum for prediction types."""
    CATEGORICAL = "categorical"
    REGRESSION = "numerical"
