from __future__ import annotations
import typing as t
from collections import ChainMap
from starlette.requests import Request
from starlette.responses import Response

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame


def guess_media_type(request: Request, *, default="application/json") -> str:
    format = request.query_params.get("format")
    if format == "html":
        return "text/html"
    elif format == "csv":
        return "text/csv"
    elif format == "tsv":
        return "text/tsv"
    elif format == "markdown" or format == "md":
        return "text/markdown"
    elif format == "json":
        return "application/json"

    content_type = request.headers.get("content-type")
    if content_type is not None:
        return content_type
    return default


class DataFrameResponse(Response):
    media_type = "application/json"
    to_params_default = {"to_json_orient": "records"}

    def __init__(self, *args: t.Tuple[t.Any], **kwargs: t.Dict[str, t.Any]) -> None:
        self._to_params = ChainMap(
            {k: kwargs.pop(k) for k in list(kwargs.keys()) if k.startswith("to_")},
            self.__class__.to_params_default,
        )
        super().__init__(*args, **kwargs)

    def render(self, df: DataFrame) -> bytes:
        if self.media_type == "text/markdown":
            i = len("to_markdown") + 1
            kwargs = {
                k[i:]: v
                for k, v in self._to_params.items()
                if k.startswith("to_markdown")
            }
            return super().render(df.to_markdown(**kwargs))
        elif self.media_type == "text/html":
            i = len("to_html") + 1
            kwargs = {
                k[i:]: v for k, v in self._to_params.items() if k.startswith("to_html")
            }
            return super().render(df.to_html(**kwargs))
        elif self.media_type == "text/csv" or self.media_type == "text/tsv":
            i = len("to_csv") + 1
            kwargs = {
                k[i:]: v for k, v in self._to_params.items() if k.startswith("to_csv")
            }
            if self.media_type == "text/tsv":
                kwargs["sep"] = "\t"
            return super().render(df.to_csv(**kwargs))
        else:
            i = len("to_json") + 1
            kwargs = {
                k[i:]: v for k, v in self._to_params.items() if k.startswith("to_json")
            }
            return super().render(df.to_json(**kwargs))
