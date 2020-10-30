from __future__ import annotations
import typing as t

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from . import DataFrameResponse, guess_media_type

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame


async def list_dataset(request: Request):
    import importlib.resources

    r = []
    with importlib.resources.path("vega_datasets", "_data") as path:
        for fpath in path.glob("*.json"):
            name = fpath.with_suffix("").name
            r.append(
                {name: app.url_path_for("get_dataset", data=name), "method": "GET"}
            )
    return JSONResponse(r)


async def get_dataset(request: Request):
    from vega_datasets import data

    df: DataFrame = getattr(data, request.path_params["data"])()
    return DataFrameResponse(df, media_type=guess_media_type(request))


async def get_dataset_describe(request: Request):
    from vega_datasets import data

    df: DataFrame = getattr(data, request.path_params["data"])()
    return DataFrameResponse(
        df.describe(), to_json_orient="columns", media_type=guess_media_type(request)
    )


async def get_dataset_columns(request: Request):
    from vega_datasets import data

    df: DataFrame = getattr(data, request.path_params["data"])()
    columns = dict(zip(df.dtypes.index, df.dtypes.map(str)))
    return JSONResponse({"dataset": request.path_params["data"], "columns": columns})


async def get_dataset_aggs(request: Request):
    from vega_datasets import data

    field = request.path_params["field"]
    fns = request.query_params.getlist("fn")
    if len(fns) == 0:
        fns = ["min", "max", "mean"]

    df: DataFrame = getattr(data, request.path_params["data"])()

    grouped_df: DataFrame = (
        df.groupby(by=request.path_params["by"]).agg({field: fns}).reset_index()
    )

    # flat index
    grouped_df.columns = grouped_df.columns.to_flat_index()
    grouped_df.columns = grouped_df.columns.map(
        lambda xs: xs[0] if not xs[-1] else "-".join(xs)
    )
    return DataFrameResponse(
        grouped_df, media_type=request.headers.get("content-type"),
    )


app = Starlette(
    debug=True,
    routes=[
        Route("/", list_dataset),
        Route("/{data}", get_dataset),
        Route("/{data}/describe", get_dataset_describe),
        Route("/{data}/columns", get_dataset_columns),
        Route("/{data}/groupby/{by}/aggs/{field}", get_dataset_aggs),
    ],
)


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(
        prog=run.__name__,
        description=run.__doc__,
        formatter_class=type(
            "_HelpFormatter",
            (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter),
            {},
        ),
    )
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument("--port", required=False, default=8888, type=int, help="-")
    parser.add_argument("--debug", required=False, action="store_true", help="-")
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


def run(*, port: int = 8888, debug: bool = False) -> None:
    import uvicorn

    uvicorn.run(app, port=port, debug=debug)


if __name__ == "__main__":
    main()
