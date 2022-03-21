# Consolidates data cleansing, schema validation, anomaly detection and transformation functions
from __future__ import annotations
from numbers import Number  # For type hint
import datetime
import cat_enum
from math import exp




def clean_numeric_missing_values(data: str, values: cat_enum.Missing) -> str:
    """
    Returns a string column with proper missing values
    :param values: Enum with missing values
    :param data: A string value
    :return clean_string: A string value with proper Numpy NaN missing value
    """
    if hasattr(values, data):
        data = "NaN"
    return data


def validate_float(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_discrete(value) -> bool:
    try:
        int(str(value))
        return True
    except ValueError:
        return False


def validate_date(date_str: str) -> bool:
    if type(date_str) != str:
        return False
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def range_anomalies(data: Number, lower_range: Number, upper_range: Number) -> bool:
    if data < lower_range or data > upper_range:
        return False
    else:
        return True


def categorical_value_anomalies(data: str, values: cat_enum.Enum) -> bool:
    if hasattr(values, data):
        return True
    else:
        return False


def math_transform_column(column_x: float, column_y: float) -> float:
    return column_x ** 3 + exp(column_y)
