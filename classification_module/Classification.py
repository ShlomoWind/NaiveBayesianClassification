from functools import total_ordering

from data_module.Data_Loader import DataLoader

loader = DataLoader('csv','buy_computer_data.csv')
df = loader.load()

classes = df.index.unique()
total_count = len(df)
class_probs = {cls: (df.index == cls).sum() / total_count for cls in classes }

probabilities = {}
for column in df.columns:
    if column == 'buys_computer':
        continue
    grouped = df.groupby(['buys_computer', column]).size()
    cls_count = df['buys_computer'].value_counts()
    column_values = df[column].unique()
    probabilities[column] = {}
    for value in column_values:
        probabilities[column][value] = {}
        for cls in classes:
            count = grouped[(cls, value)] if (cls, value) in grouped else 0
            total = cls_count[cls]
            prob = count / total
            probabilities[column][value][cls] = prob

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