from __future__ import annotations
import typing as t
import typing_extensions as tx

if t.TYPE_CHECKING:
    from pandas.core.frame import DataFrame


@tx.runtime_checkable
class DatasetProvider(tx.Protocol):
    def provide_dataset(self, name: str) -> DataFrame:
        ...

    def list_dataset_names(self, name: str) -> t.List[str]:
        ...


class VegaDatasetProvider:
    def list_dataset_names(self) -> t.List[str]:
        from vega_datasets import data

        return data.list_datasets()

    def provide_dataset(self, name: str) -> DataFrame:
        from vega_datasets import data

        return getattr(data, name)()


vega_dataset_provider = VegaDatasetProvider()


class FunctionDatasetProvider:
    def __init__(self, provide: t.Callable[[], DataFrame]) -> None:
        self.provide = provide

    def list_dataset_names(self) -> t.List[str]:
        return [self.provide.__name__]

    def provide_dataset(self, name: str) -> DataFrame:
        return self.provide()


def fake() -> DataFrame:
    import pandas as pd

    return pd.DataFrame({"name": ["foo", "bar", "baz"], "age": [20, 20, 0]})


fake_dataset_provider = FunctionDatasetProvider(fake)
