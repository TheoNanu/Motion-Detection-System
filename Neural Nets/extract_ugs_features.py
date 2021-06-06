import pandas as pd
df = pd.read_csv('C:\\Users\\theod\\OneDrive\\Documente\\features.csv', header=0)
print(df.columns[0])
# df_new = df.iloc[:, [0, 4, 5, 12, 16, 17, 18]]
# #df_new = df_new[df["Label"] == 3 or df["Label"] == 4]
# header = ["leftCountLeft", "leftGestureStartTime", "leftGestureStopTime", "rightCounterLeft", "rightGestureStartTime",
#           "rightGestureStopTime", "Label"]
# df_new.to_csv("extracted_features.csv", index=False, header=header)