from user_module.user_input import data_info,column_for_prediction
from data_module.Data_Loader import DataLoader
from classification_module.Classification import train,predict
from testing_module.Tester import accuracy_check
from clining_module.Cliner import clean_data
from sklearn.model_selection import train_test_split

def ran():
    path, type = data_info()
    loader = DataLoader(type,path)
    df = loader.load()
    df = clean_data(df)
    column = column_for_prediction(df)
    df.set_index(column,inplace=True)
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df.index)
    class_probs, probabilities = train(train_df)
    accuracy = accuracy_check(test_df, predict, class_probs, probabilities)
    print(f"\n✅ Accuracy on test set: {accuracy:.2%}")
