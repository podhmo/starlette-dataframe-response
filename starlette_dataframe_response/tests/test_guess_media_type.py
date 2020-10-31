# type:ignore
from __future__ import annotations
import pytest

from starlette_dataframe_response import guess_media_type as _callFUT


@pytest.mark.parametrize(
    "want, input",
    [
        ("application/json", {"headers": {}, "query_string": {}}),
        ("application/json", {"headers": {}, "query_string": {"format": "json"}}),
        ("text/csv", {"headers": {}, "query_string": {"format": "csv"}}),
        ("text/markdown", {"headers": {}, "query_string": {"format": "markdown"}}),
        ("text/markdown", {"headers": {}, "query_string": {"format": "md"}}),
        (
            "text/csv",
            {"headers": [(b"content-type", b"text/csv")], "query_string": {},},
        ),
        (
            "text/markdown",
            {
                "headers": [(b"content-type", b"text/csv")],
                "query_string": {"format": "markdown"},
            },
        ),
    ],
)
def test_guess_params(want, input):
    from starlette.requests import Request

    scope = {"type": "http", **input}
    got = _callFUT(Request(scope))
    assert want == got
