import json
from typing import List
import pandas


MaxNBars = 500


class XSeries:
    def __init__(self, series: pandas.Series, name: str):
        self.series = series
        self.name = name


class YSeries:
    def __init__(self, series: pandas.Series, name: str, color: str):
        self.series = series
        self.name = name
        self.color = color


class SeriesParams:
    """
    Fully-sane parameters. Columns are series.
    """
    def __init__(self, *, title: str, x_axis_label: str, y_axis_label: str,
                 x_series: XSeries, y_columns: List[YSeries]):
        self.title = title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.x_series = x_series
        self.y_columns = y_columns

    def to_vega_data_values(self):
        """Build a dict for Vega's .data.values Array"""
        def build_record(i):


class YColumn:
    def __init__(self, column: str, color: str):
        self.column = column
        self.color = color


class UserParams:
    """
    Parameter dict specified by the user: valid types, unchecked values.
    """
    def __init__(self, params):
        self.title = str(params.get('title', ''))
        self.x_axis_label = str(params.get('x_axis_label', ''))
        self.y_axis_label = str(params.get('y_axis_label', ''))
        self.x_column = str(params.get('x_column', ''))
        self.y_columns = UserParams.parse_y_columns(
            params.get('y_columns', 'null')
        )

    def validate_with_table(self, table: pandas.DataFrame) -> SeriesParams:
        """
        Create a SeriesParams ready for charting, or raises ValueError.

        Features ([tested?]):
        [ ] Error if too many bars
        [ ] Error if X column is missing
        [ ] Error if no Y columns chosen
        [ ] Error if a Y column is missing
        [ ] Error if a Y column is the X column
        """
        if len(table.index) >= MaxNBars:
            raise ValueError(
                f'Refusing to build column chart with '
                'more than {MaxNBars} bars'
            )

        if self.x_column not in table.columns:
            raise ValueError('Please choose an X-axis column')
        if not self.y_columns:
            raise ValueError('Please choose a Y-axis column')

        x_series = XSeries(table[self.x_column].astype(str), self.x_column)

        y_series = []
        for ycolumn in self.y_columns:
            if ycolumn.column not in table.columns:
                raise ValueError(
                    f'Cannot plot Y-axis column {ycolumn.column} '
                    'because it does not exist'
                )
            elif ycolumn.column == self.x_column:
                raise ValueError(
                    f'You cannot plot Y-axis column {ycolumn.column} '
                    'because it is the X-axis column'
                )

            series = table[ycolumn.column]
            floats = pandas.to_numeric(series, errors='coerce')
            floats.fillna(0.0)
            y_series.append(YSeries(floats, ycolumn.column, ycolumn.color))

        return SeriesParams(title=self.title, x_axis_label=self.x_axis_label,
                            y_axis_label=self.y_axis_label, x_series=x_series,
                            y_series=y_series)


    @staticmethod
    def parse_y_columns(s):
        try:
            arr = json.parse(s)
            return [YColumn(str(o.get('column', '')),
                            str(o.get('color', '#000000')))
                    for o in arr]
        except json.decoder.JSONDecodeError:
            # Not valid JSON
            return []
        except TypeError:
            # arr is not iterable
            return []
        except AttributeError:
            # an element of arr is not a dict
            return []


def render(table, params):
    user_params = UserParams.from_params(params)
    try:
        valid_params = user_params.validate_with_table(table)
    except ValueError as err:
        return (table, str(err), {})


    json_dict = {
        '$schema': 'https://vega.github.io/schema/vega-lite/v2.0.json',
        'data': {'values': values},
    }

    return (table, error, json_dict)
