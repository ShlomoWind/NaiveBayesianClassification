class TrainModel:
    def __init__(self):
        self.class_probs = None
        self.probabilities = None

    def train(self,df):
        classes = df.index.unique()
        total_count = len(df)
        if total_count == 0:
            raise ValueError("Training dataframe is empty")
        self.class_probs = {cls: (df.index == cls).sum() / total_count for cls in classes}

        self.probabilities = {}
        for column in df.columns:
            column_values = df[column].unique()
            self.probabilities[column] = {}
            grouped = df.groupby([df.index, column]).size()
            cls_count = df.index.value_counts()

            for value in column_values:
                self.probabilities[column][value] = {}

                for cls in classes:
                    count = grouped.get((cls, value), 0)
                    total = cls_count[cls]
                    prob = count / total
                    self.probabilities[column][value][cls] = prob

        return self.class_probs, self.probabilities