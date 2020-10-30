def pokemon():
    import pandas as pd
    import pathlib

    return pd.read_csv(pathlib.Path(__file__).parent / "pokemon.csv")
