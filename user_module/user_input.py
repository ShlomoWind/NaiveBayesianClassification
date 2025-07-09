import pandas as pd

def data_info():
    data_path = input("").strip()
    data_type = input("").strip().lower()
    return data_path,data_type

def column_for_prediction(data_frame):
    print("Available columns:", list(data_frame.columns))
    print("=================")
    column = input("Which column do you want to use as the target? ").strip()
    return column

