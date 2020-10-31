PORT ?= 8888

# check with httpie
# http -v :8888/
# http -v :8888/iris
# http -v :8888/cars
# http -v :8888/iris format==csv
# http -v :8888/iris to_json_orient==columns
# http -v :8888/iris/columns
# http -v :8888/iris/describe
# http -v :8888/iris/groupby/species/aggs/sepalWidth
# http -v :8888/iris/groupby/species/aggs/sepalWidth fn==min fn==max fn==std fn==mean fn==count
# http -v :8888/iris/groupby/species/aggs/sepalWidth,sepalLength
run:
	python -m starlette_dataframe_response --port $(PORT)
.PHONY: run

list_dataset.json:
	http -b :8888/ | jq . | tee $@

