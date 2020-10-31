# type:ignore
from __future__ import annotations
import pytest

from starlette_dataframe_response import guess_params as _callFUT


@pytest.mark.parametrize(
    "want, input, options",
    [
        (
            {"to_json_orient": "columns"},
            {"media_type": "application/json", "to_json_orient": "columns"},
            {},
        ),
        (
            {"orient": "columns"},
            {"media_type": "application/json", "to_json_orient": "columns"},
            {"trim": True},
        ),
    ],
)
def test_guess_params(want, input, options):
    got = _callFUT(input.items(), prefix="to_json", **options)
    assert want == got
