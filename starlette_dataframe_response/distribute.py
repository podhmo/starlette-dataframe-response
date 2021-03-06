from __future__ import annotations
import typing as t

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from . import DataFrameResponse
from .dataset import vega_dataset_provider, DatasetProvider, FunctionDatasetProvider

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame
    from starlette.responses import Response


async def list_dataset(request: Request) -> Response:
    r = []
    for name in app.dataset_provider.list_dataset_names():
        r.append({name: app.url_path_for("get_dataset", data=name), "method": "GET"})
    return JSONResponse(r)


async def get_dataset(request: Request) -> Response:
    df: DataFrame = app.dataset_provider.provide_dataset(request.path_params["data"])
    return DataFrameResponse.from_request(request, df)


async def get_dataset_describe(request: Request) -> Response:
    df: DataFrame = app.dataset_provider.provide_dataset(request.path_params["data"])
    return DataFrameResponse.from_request(
        request, df.describe(), to_json_orient="columns"
    )


async def get_dataset_columns(request: Request) -> Response:
    df: DataFrame = app.dataset_provider.provide_dataset(request.path_params["data"])
    columns = dict(zip(df.dtypes.index, df.dtypes.map(str)))
    return JSONResponse({"dataset": request.path_params["data"], "columns": columns})


async def get_dataset_aggs(request: Request) -> Response:
    fields = [request.path_params["field"]]
    fns = request.query_params.getlist("fn")
    if len(fns) == 0:
        fns = ["min", "max", "mean"]

    df: DataFrame = app.dataset_provider.provide_dataset(request.path_params["data"])

    if "," in fields[0]:
        fields = [f.strip() for f in fields[0].split(",")]

    grouped_df: DataFrame = (
        df.groupby(by=request.path_params["by"])
        .agg({f: fns for f in fields})
        .reset_index()
    )

    # flat index
    grouped_df.columns = grouped_df.columns.to_flat_index()
    grouped_df.columns = grouped_df.columns.map(
        lambda xs: xs[0] if not xs[-1] else "-".join(xs)
    )
    return DataFrameResponse.from_request(request, grouped_df)


if t.TYPE_CHECKING:
    import typing_extensions as tx

    class App(tx.Protocol):
        dataset_provider: DatasetProvider

        def url_path_for(self, name: str, **params: t.Any) -> str:
            ...


app: App = Starlette(  # type:ignore
    debug=True,
    routes=[
        Route("/", list_dataset),
        Route("/{data}", get_dataset),
        Route("/{data}/describe", get_dataset_describe),
        Route("/{data}/columns", get_dataset_columns),
        Route("/{data}/groupby/{by}/aggs/{field}", get_dataset_aggs),
    ],
)
app.dataset_provider = vega_dataset_provider


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
    parser.add_argument(
        "--dataset-provider",
        required=False,
        help="-",
        default="starlette_dataframe_response.dataset.vega_dataset_provider",
    )
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


def run(
    *, port: int = 8888, debug: bool = False, dataset_provider: t.Optional[str] = None,
) -> None:
    import uvicorn

    if dataset_provider is not None:
        try:
            from magicalimport import import_module
        except ImportError:
            from importlib import import_module  # type:ignore # noqa
        sep = ":"
        if sep not in dataset_provider:
            sep = "."
        mod, name = dataset_provider.rsplit(sep, 1)

        provider = getattr(import_module(mod), name)
        if not isinstance(provider, DatasetProvider):
            provider = FunctionDatasetProvider(provider)
        app.dataset_provider = provider
    uvicorn.run(app, port=port, debug=debug)


if __name__ == "__main__":
    main()
