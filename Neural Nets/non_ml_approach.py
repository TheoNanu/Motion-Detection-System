import pandas as pd


def votingSystem(row):
    leftActivatedFirst = False
    leftPeakFirst = False
    leftDeactivatedFirst = False

    if row['leftGestureStartTime'] < row['rightGestureStartTime']:
        leftActivatedFirst = True

    if row['leftCountLeft'] < row['rightCounterLeft']:
        leftPeakFirst = True

    if row['leftGestureStopTime'] < row['rightGestureStopTime']:
        leftDeactivatedFirst = True

    if (leftPeakFirst or leftDeactivatedFirst) and leftActivatedFirst:
        return 0
    else:
        return 1


if __name__ == '__main__':
    df = pd.read_csv('left_and_right_samples.csv')
    numberOfFeatures = df.shape[1] - 1

    print('Dataset size: ' + str(int(df.size / (numberOfFeatures + 1))))
    print('Test set size: ' + str(int(0.3 * df.size / (numberOfFeatures + 1)) + 1))

    testSetSize = int(0.3 * df.size / (numberOfFeatures + 1)) + 1
    correctPredictions = 0

    print(int(df.size / (numberOfFeatures + 1)) - testSetSize)

    test_df = df.iloc[int(df.size / (numberOfFeatures + 1)) - testSetSize:, :]
    print(test_df.size / (numberOfFeatures + 1))
    print(test_df.shape)
    comparisons = 0

    for i in range(0, int(test_df.size / (numberOfFeatures + 1))):
        res = votingSystem(test_df.iloc[i, 0:numberOfFeatures].to_dict())
        comparisons += 1
        print('Voting system prediction was ' + str(res) + ' while the actual value is ' + str(test_df.iloc[i, numberOfFeatures]))
        if res == test_df.iloc[i, numberOfFeatures]:
            print('Prediction was correct')
            correctPredictions += 1
        else:
            print('Prediction was wrong')

    accuracy = correctPredictions / testSetSize

    print("The accuracy for the non ml approach is " + str(accuracy))
    print("Comparisons " + str(comparisons))
