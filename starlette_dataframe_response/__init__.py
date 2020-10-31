from __future__ import annotations
import typing as t
from collections import ChainMap
from starlette.requests import Request
from starlette.responses import Response

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame


def guess_media_type(request: Request, *, default: str = "application/json") -> str:
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

    content_type: str = request.headers.get("content-type")
    if content_type is not None:
        return content_type
    return default


def guess_params(
    items: t.Iterable[t.Tuple[str, t.Any]], *, prefix: str, trim: bool = False
) -> t.Dict[str, t.Any]:
    if trim:
        i = len(prefix) + 1
        return {k[i:]: v for k, v in items if k.startswith(prefix)}
    else:
        return {k: v for k, v in items if k.startswith(prefix)}


class DataFrameResponse(Response):
    media_type = "application/json"
    to_params_default = {"to_json_orient": "records"}

    @classmethod
    def from_request(
        cls, request: Request, df: DataFrame, *args: t.Any, **kwargs: t.Any
    ) -> DataFrameResponse:
        params = guess_params(request.query_params.items(), prefix="to_")
        params.update(kwargs)

        if "media_type" not in kwargs:
            params["media_type"] = guess_media_type(request)
        return cls(df, *args, **params)

    def __init__(self, df: DataFrame, *args: t.Any, **kwargs: t.Any) -> None:
        self._to_params = ChainMap(
            {k: kwargs.pop(k) for k in list(kwargs.keys()) if k.startswith("to_")},
            self.__class__.to_params_default,
        )
        super().__init__(df, *args, **kwargs)

    def render(self, df: DataFrame) -> bytes:
        if self.media_type == "text/markdown":
            kwargs = guess_params(
                self._to_params.items(), prefix="to_markdown", trim=True
            )
            return super().render(df.to_markdown(**kwargs))
        elif self.media_type == "text/html":
            kwargs = guess_params(self._to_params.items(), prefix="to_html", trim=True)
            return super().render(df.to_html(**kwargs))
        elif self.media_type == "text/csv" or self.media_type == "text/tsv":
            kwargs = guess_params(self._to_params.items(), prefix="to_csv", trim=True)
            if self.media_type == "text/tsv":
                kwargs["sep"] = "\t"
            return super().render(df.to_csv(**kwargs))
        else:
            kwargs = guess_params(self._to_params.items(), prefix="to_json", trim=True)
            return super().render(df.to_json(**kwargs))
