PORT ?= 8888

# check with httpie
# http -v :8888/
# http -v :8888/pokemon
# http -v :8888/pokemon format==csv
# http -v :8888/pokemon/columns
# http -v :8888/pokemon/describe
# http -v :8888/pokemon/groupby/generation/aggs/base_total
# http -v :8888/pokemon/groupby/type1/aggs/base_total fn==min fn==max fn==std fn==mean fn==count
run: pokemon.csv
	python -m starlette_dataframe_response --dataset-provider ./data.py:pokemon

pokemon.csv:
	wget https://gist.githubusercontent.com/leoyuholo/b12f882a92a25d43cf90e29812639eb3/raw/1abee7fb529dfacb374633f3a450b37634f8321a/pokemon.csv
