import pandas as pd

def data_info():
    data_path = input("Enter path to data file: ").strip()
    data_type = input("Enter data source type - (csv,sql,excel,json): ").strip().lower()
    if data_type not in ['csv', 'sql', 'excel', 'json']:
        raise ValueError(f"Unsupported data source type: {data_type}")
    return data_path,data_type

def column_for_prediction(data_frame):
    print(f"\nAvailable columns: \n{list(data_frame.columns)}")
    print("=================")
    column = input("Which column do you want to use as the target? ").strip()
    print("=================")
    return column

