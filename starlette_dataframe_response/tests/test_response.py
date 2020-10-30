# type:ignore
from __future__ import annotations
import typing as t
import pandas as pd

if t.TYPE_CHECKING:
    from starlette_dataframe_response import DataFrameResponse


def _makeOne(df: pd.DataFrame, **kwargs: t.Dict[str, t.Any]) -> DataFrameResponse:
    from starlette_dataframe_response import DataFrameResponse

    return DataFrameResponse(df, **kwargs)


########################################
# json
########################################
def test_json__with_orient_default():
    df = pd.DataFrame({"name": ["foo", "bar"], "age": [20, 0]})
    got = _makeOne(df).body
    want = b'[{"name":"foo","age":20},{"name":"bar","age":0}]'
    assert want == got


def test_json__with_orient_columnns():
    df = pd.DataFrame({"name": ["foo", "bar"], "age": [20, 0]})
    got = _makeOne(df, to_json_orient="columns").body
    want = b'{"name":{"0":"foo","1":"bar"},"age":{"0":20,"1":0}}'
    assert want == got


def test_json__with_orient_records():
    df = pd.DataFrame({"name": ["foo", "bar"], "age": [20, 0]})
    got = _makeOne(df, to_json_orient="records").body
    want = b'[{"name":"foo","age":20},{"name":"bar","age":0}]'
    assert want == got


def test_json__with_date_format_default():
    from datetime import date

    df = pd.DataFrame({"now": [date(2000, 1, 1)]})
    got = _makeOne(df).body
    want = b'[{"now":946684800000}]'
    assert want == got


def test_json__with_date_format_iso():
    from datetime import date

    df = pd.DataFrame({"now": [date(2000, 1, 1)]})
    got = _makeOne(df, to_json_date_format="iso").body
    want = b'[{"now":"2000-01-01T00:00:00.000Z"}]'
    assert want == got


########################################
# markdown
########################################
def test_markdown():
    df = pd.DataFrame({"name": ["foo", "bar"], "age": [20, 0]})
    got = _makeOne(df, media_type="text/markdown").body
    want = b"""\
|    | name   |   age |
|---:|:-------|------:|
|  0 | foo    |    20 |
|  1 | bar    |     0 |"""
    assert want == got
