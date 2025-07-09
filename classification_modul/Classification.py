import pandas as pd

df = pd.read_csv('../buy_computer_data.csv')

classes = df['buys_computer'].unique()

class_probs = {} #General probabilities of the categories (yes, no)
total_count = len(df)

for cls in classes:
    class_count = len(df[df['buys_computer'] == cls])
    class_probs[cls] = class_count / total_count

probabilities = {} #Conditional probabilities of each value for each column in each category

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