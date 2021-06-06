import pandas as pd
df = pd.read_csv('extracted_features.csv', header=0)
df_new = df.iloc[:, :]
df_new = df_new[(df["Label"] == 3) | (df["Label"] == 4)]
#print(df_new)
df_new = df_new.replace(4, 1)
df_new = df_new.replace(3, 0)
print(df_new)
df_new.to_csv("left_and_right_samples.csv", index=False)