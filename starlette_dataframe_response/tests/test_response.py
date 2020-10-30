from __future__ import annotations
import typing as t
import pandas as pd

if t.TYPE_CHECKING:
    from starlette_dataframe_response import DataFrameResponse


def _makeOne(df: pd.DataFrame, **kwargs: t.Dict[str, t.Any]) -> DataFrameResponse:
    from starlette_dataframe_response import DataFrameResponse

    return DataFrameResponse(df, **kwargs)


def test_json():
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
