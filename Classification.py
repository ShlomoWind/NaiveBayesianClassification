import pandas as pd

df = pd.read_csv('buy_computer_data.csv')

classes = df['buys_computer'].unique()

class_probs = {}
total_count = len(df)

for cls in classes:
    class_count = len(df[df['buys_computer'] == cls])
    class_probs[cls] = class_count / total_count

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
            count = grouped.get((cls, value),0)
            total = cls_count[cls]
            prob = count / total
            probabilities[column][value][cls] = prob
