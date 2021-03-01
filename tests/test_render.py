from collections import namedtuple

import numpy as np
import pandas as pd

from columnchart import render

DefaultParams = {
    "title": "",
    "x_axis_label": "",
    "y_axis_label": "",
    "x_column": "",
    "y_columns": [],
}


Column = namedtuple("Column", ("name", "type", "format"))


def P(**kwargs):
    """Easily build params, falling back to defaults."""
    assert not (set(kwargs.keys()) - set(DefaultParams.keys()))
    return {
        **DefaultParams,
        **kwargs,
    }


def test_happy_path():
    dataframe, error, json_dict = render(
        pd.DataFrame(
            {
                "A": ["foo", "bar"],
                "B": [1, 2],
                "C": [2, 3],
            }
        ),
        P(
            x_column="A",
            y_columns=[
                {"column": "B", "color": "#bbbbbb"},
                {"column": "C", "color": "#cccccc"},
            ],
        ),
        input_columns={
            "A": Column("A", "text", None),
            "B": Column("B", "number", "{:,}"),
            "C": Column("C", "number", "{:,f}"),
        },
    )
    # Check values
    assert json_dict["data"]["values"] == [
        dict(x="foo", y0=1, y1=2),
        dict(x="bar", y0=2, y1=3),
    ]
    assert json_dict["transform"][1]["from"]["data"]["values"] == [
        dict(key="y0", series="B"),
        dict(key="y1", series="C"),
    ]
    # Check axis format is first Y column's format
    assert json_dict["config"]["axisY"]["format"] == ",r"


def test_output_nulls():
    dataframe, error, json_dict = render(
        pd.DataFrame(
            {
                "A": ["foo", "bar", None],
                "B": [np.nan, 2, 3],
                "C": [2, 3, 4],
            }
        ),
        P(
            x_column="A",
            y_columns=[
                {"column": "B", "color": "#bbbbbb"},
                {"column": "C", "color": "#cccccc"},
            ],
        ),
        input_columns={
            "A": Column("A", "text", None),
            "B": Column("B", "number", "{:,}"),
            "C": Column("C", "number", "{:,f}"),
        },
    )
    # Check values
    assert json_dict["data"]["values"] == [
        dict(x="foo", y0=None, y1=2),
        dict(x="bar", y0=2, y1=3),
        # None row is removed
    ]
