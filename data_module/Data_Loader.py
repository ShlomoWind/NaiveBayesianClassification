import pandas as pd

class DataLoader:
    def __init__(self,type,path):
        self.type = type
        self.path = path

    def load(self):
        if self.type == 'csv':
            return self.csv_loader()
        if self.type == 'json':
            return self.json_loader()
        if self.type == 'sql':
            return self.sql_loader()
        else:
            raise ValueError("type error")

    def csv_loader(self):
        df = pd.read_csv(self.path)
        return df

    def json_loader(self):
        pass

    def sql_loader(self):
        pass