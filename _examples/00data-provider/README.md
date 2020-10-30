## `--data-provider` example

this is the example using `--data-provider` option, with below pokemon dataset.

- https://gist.github.com/leoyuholo/b12f882a92a25d43cf90e29812639eb3

```console
# prepare
# pip install starlette_dataframe_response[fullset]

$ python -m starlette_dataframe_response --dataset-provider ./data.py:pokemon
INFO:     Started server process [91092]
INFO:     Uvicorn running on http://127.0.0.1:8888 (Press CTRL+C to quit)
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56848 - "GET /pokemon HTTP/1.1" 200 OK
INFO:     127.0.0.1:56851 - "GET /pokemon HTTP/1.1" 200 OK
INFO:     127.0.0.1:56853 - "GET /pokemon/columns HTTP/1.1" 200 OK
INFO:     127.0.0.1:56855 - "GET /pokemon/describe HTTP/1.1" 200 OK
INFO:     127.0.0.1:56857 - "GET /pokemon/columns HTTP/1.1" 200 OK
INFO:     127.0.0.1:56860 - "GET /pokemon/groupby/generation/aggs/base_total HTTP/1.1" 200 OK
INFO:     127.0.0.1:56866 - "GET /pokemon/groupby/type1/aggs/base_total?fn=min&fn=max&fn=std&fn=mean&fn=count HTTP/1.1" 200 OK
INFO:     127.0.0.1:56868 - "GET /pokemon/groupby/type1/aggs/base_total?fn=min&fn=max&fn=std&fn=mean&fn=count HTTP/1.1" 200 OK
INFO:     127.0.0.1:56870 - "GET /pokemon/groupby/type1/aggs/base_total?fn=min&fn=max&fn=std&fn=mean&fn=count HTTP/1.1" 200 OK
```
