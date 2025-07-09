import pandas as pd

class DataLoader:
    def __init__(self,type,path):
        self.type = type
        self.path = path

    def load(self):
        if self.type == 'csv':
            return self.csv_loader()

    def csv_loader(self):
        df = pd.read_csv(self.path)
        print("Available columns:", list(df.columns))
        target_column = input("Which column do you want to use as the target? ").strip()
        df.set_index(target_column,inplace=True)
        return df