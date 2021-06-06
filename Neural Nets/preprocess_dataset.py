import pandas as pd
import numpy as np

df = pd.read_csv("datasets/features_remade.csv", header=0)
# df.replace([np.inf, -np.inf], np.nan, inplace=True)
# df.dropna(inplace=True)\
shuffled_df = df.sample(frac=1)
shuffled_df.to_csv("datasets/features_processed.csv", header=df.columns, index=False)