# starlette-dataframe-response

:construction: this project is under construction :construction:

Convenient, but not fast.

Resources:

* **Source**: https://github.com/podhmo/starlette-dataframe-response

### Installation 

`$ pip install starlette-dataframe-response`


### Requirements
Python 3.7+

### Dependencies

- starlette
- pandas
- (vega_datasets)
- (magicalimport)

### Example

```python
import pandas as pd
from starlette.requests import Request
from starlette_dataframe_response import DataFrameResponse, guess_media_type

async def get_dataset(request: Request):
    df: DataFrame = pd.read_csv("<some dataset>.csv")
    return DataFrameResponse(df, media_type=guess_media_type(request))

app = Starlette(
    debug=True,
    routes=[
        Route("/dataset/<some dataset>", get_dataset),
    ],
)
```


Then, supporting the request following.

```
# return dataset as json (orient=records)
GET /dataset/<some dataset>

# return dataset as csv
GET /dataset/<some dataset>?format=csv
# return dataset as markdown
GET /dataset/<some dataset>?format=markdown
# return dataset as html
GET /dataset/<some dataset>?format=html
```

If you want to customize the JSON response.

```py
# use orient="columns"
DataFrameResponse(df, media_type=guess_media_type(request), to_json_orient="columns")
```

### `python -m starlette_dataframe_response.distribute`

And It also includes an example using [vega-datasets](https://github.com/vega/vega-datasets).

```console
$ python -m starlette_dataframe_response.distribute --port 8888
```

(with httpie)

```
$ http :8888/
$ http :8888/iris
$ http :8888/iris  format==csv
$ http :8888/iris/columns
$ http :8888/iris/describe
$ http :8888/iris/groupby/species/aggs/sepalWidth
$ http :8888/iris/groupby/species/aggs/sepalWidth fn==min fn==max fn==count fn==mean fn==std
```

Or if you want to see an example using a custom data, in above included app [examples/00data-provider/](https://github.com/podhmo/starlette-dataframe-response/tree/main/_examples/00data-provider)

### Contribution
