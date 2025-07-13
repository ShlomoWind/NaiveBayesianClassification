from user_module.user_input import data_info,column_for_prediction
from data_module.Data_Loader import DataLoader
from classification_module.Classification import train,predict
from testing_module.Tester import accuracy_check
from cleaning_module.Cliner import clean_data
from sklearn.model_selection import train_test_split

def ran():
    try:
        path, type = data_info()
        loader = DataLoader(type,path)
        df = loader.load()
        df = clean_data(df)
        column = column_for_prediction(df)
        df.set_index(column,inplace=True)
        train_df, test_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df.index)
        class_probs, probabilities = train(train_df)
        accuracy = accuracy_check(test_df, predict, class_probs, probabilities)
        print(f"\n*****\nAccuracy on test set: {accuracy:.2%}\n*****")

        features = list(df.columns)
        print("\nYou can now test predictions manually.")
        print("Type 'exit' at any time to stop.\n")

        while True:
            user_sample = {}
            for feature in features:
                value = input(f"Enter value for '{feature}': ").strip()
                if value.lower() == 'exit':
                    print("Exiting prediction loop.")
                    return
                user_sample[feature] = value

            prediction = predict(user_sample, class_probs, probabilities)
            print(f"Prediction for the given input: {prediction}\n")
    except Exception as e:
        print(f"Error: {e}")