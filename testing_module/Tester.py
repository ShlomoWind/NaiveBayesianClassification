from random import sample

def accuracy_check(test_df, predict, class_probs, probabilities):
    if len(test_df) == 0:
        raise ValueError("Test dataframe is empty")
    correct_counter = 0
    total = len(test_df)
    for index, row in test_df.iterrows():
        features  = row.to_dict()
        predicted = predict(features,class_probs,probabilities)
        if predicted == index:
            correct_counter += 1
    return correct_counter / len(test_df)

