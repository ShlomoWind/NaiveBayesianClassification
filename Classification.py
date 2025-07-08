import pandas as pd

df = pd.read_csv('buy_computer_data.csv')
classes = df['buys_computer'].unique()
classes_subset = {}

for cls in classes:
    subset = df[df['buys_computer'] == cls]
    classes_subset[cls] = subset

probabilities = {}
for cls,subset in classes_subset.items():
    column_dict = {}
    for column in subset.columns:
        if column == 'buys_computer':
            continue
        value_count = subset[column].value_counts(normalize=True)
        column_dict[column] = value_count.to_dict()
    probabilities[cls] = column_dict