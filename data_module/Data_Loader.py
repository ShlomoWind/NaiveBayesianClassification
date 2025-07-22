import pandas as pd

class DataLoader:
    def __init__(self,file_type,file_path):
        self.file_type = file_type
        self.file_path = file_path

    def load(self):
        try:
            if self.file_type == 'csv':
                return self.csv_loader()
            if self.file_type == 'json':
                return self.json_loader()
            if self.file_type == 'excel':
                return self.excel_loader()
            else:
                raise ValueError(f"Unsupported file type: {self.file_type}")

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at path: {self.file_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load data: {str(e)}")


    def csv_loader(self):
        df = pd.read_csv(self.file_path)
        return df

    def json_loader(self):
        df = pd.read_json(self.file_path)
        return  df

    def excel_loader(self):
        df = pd.read_excel(self.file_path)
        return df