from setuptools import setup, find_packages


install_requires = ["starlette", "pandas", "typing_extensions"]
dev_requires = ["black", "flake8", "mypy"]
tests_requires = ["pytest", "tabulate"]
fullset_requires = [
    # for to_markdown()
    "tabulate",
    # for distribute
    "vega_datasets",
    "uvicorn",
]
setup(
    classifiers=[
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">3.7",
    packages=find_packages(exclude=["starlette_dataframe_response.tests"]),
    install_requires=install_requires,
    extras_require={
        "testing": tests_requires,
        "dev": dev_requires,
        "fullset": fullset_requires,
    },
    tests_require=tests_requires,
    test_suite="starlette_dataframe_response.tests",
    #     entry_points="""
    #       [console_scripts]
    #       starlette-dataframe-response = starlette_dataframe_response.cli:main
    # """,
)
