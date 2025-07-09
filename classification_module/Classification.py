def train(df):
    classes = df.index.unique()
    total_count = len(df)
    class_probs = {cls: (df.index == cls).sum() / total_count for cls in classes}

    probabilities = {}
    for column in df.columns:
        column_values = df[column].unique()
        probabilities[column] = {}
        grouped = df.groupby([df.index,column]).size()
        cls_count = df.index.value_counts()

        for value in column_values:
            probabilities[column][value] = {}

            for cls in classes:
                count = grouped.get((cls, value), 0)
                total = cls_count[cls]
                prob = count / total
                probabilities[column][value][cls] = prob

    return class_probs,probabilities


def predict(sample,class_probs,probabilities):
    scores = {}
    for cls in class_probs:
        prob = class_probs[cls]
        for feature,value in sample.items():
            if feature in probabilities and value in probabilities[feature]:
                prob *= probabilities[feature][value].get(cls,1e-6)
            else:
                prob *= 1e-6
        scores[cls] = prob
    return max(scores, key=scores.get)