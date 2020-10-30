from __future__ import annotations
import typing as t
from starlette.requests import Request
from starlette.responses import Response

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame


def guess_media_type(request: Request, *, default="application/json") -> str:
    format = request.query_params.get("format")
    if format == "html":
        return "text/html"
    if format == "markdown" or format == "md":
        return "text/markdown"
    elif format == "json":
        return "application/json"

    content_type = request.headers.get("content-type")
    if content_type is not None:
        return content_type
    return default


class DataFrameResponse(Response):
    media_type = "application/json"

    def __init__(self, *args: t.Tuple[t.Any], **kwargs: t.Dict[str, t.Any]) -> None:
        self.to_json_orient = kwargs.pop("to_json_orient", "records")
        super().__init__(*args, **kwargs)

    def render(self, df: DataFrame) -> bytes:
        if self.media_type == "text/markdown":
            return super().render(df.to_markdown())
        elif self.media_type == "text/html":
            return super().render(df.to_html())
        return super().render(df.to_json(orient=self.to_json_orient))
