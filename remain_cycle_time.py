#import libraries
import pandas as pd
import numpy as np
import ydata_profiling as pp
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt


#load data
def load_data(filename):
    df = pd.read_csv(filename)
    df.columns = ['queues_initial_conditions', 'processing_time_machines',
       'part_of_interest_current_queue', 'part_of_interest_current_position',
       'remaining_machines', 'part_of_interest_rct']
    
    return df


#solve initial data type issues
def string_to_list(s):
    # Remove the brackets from the string
    s = s.strip('[]')
    # Split the string on commas to create a list of substrings
    substrings = s.split(',')
    # Strip whitespace from each substring and convert to the appropriate data type
    result = [eval(sub.strip()) for sub in substrings]

    return result


# preprocess of useless columns
def process_string(df):
    df['queues_initial_conditions'] = df['queues_initial_conditions'].apply(string_to_list)
    df.drop('processing_time_machines', axis=1, inplace=True)

    return df


# generate report of files
def make_report(df,filename):
    profile = pp.ProfileReport(df,title="Report HTML")
    profile.to_file(f"profile_of_data_{filename}.html")

    return None


# process once more the columns, but do it only now because analysis needed it unprocessed
def process_relative(df):
    df_new = df.copy()
    chain_lenght = len(df_new['queues_initial_conditions'][0])
    df_new['remaining_machines'] = df['remaining_machines'] / chain_lenght
    df_new['part_of_interest_current_queue'] = df['part_of_interest_current_queue'] / chain_lenght

    return df_new


# generates one column for each queue of initial conditions 
def process_queues(df):

    df_new = df.copy()
    for column in range(len(df_new['queues_initial_conditions'][0])):
        lista_ = []
        for position in df_new['queues_initial_conditions']:
            lista_.append(position[column])
        
        df_new[f'queues_initial_conditions_{column}'] = lista_
    df_new.drop('queues_initial_conditions', axis=1, inplace=True)

    return df_new

# preprocessing - standardizing of the columns to apply the regression
def standardize_pipeline(df):
    df_new = df.copy()
    # Columns to be scaled
    columns_to_scale = ['part_of_interest_current_position', 'queues_initial_conditions_0',
                        'queues_initial_conditions_1', 'queues_initial_conditions_2',
                        'queues_initial_conditions_3', 'queues_initial_conditions_4']

    proprocess = make_pipeline(
        StandardScaler(with_mean=True, with_std=True, copy=True),
    )

    # Fit and transform pipeline on specified columns
    df_new[columns_to_scale] = proprocess.fit_transform(df_new[columns_to_scale])

    return df_new

# concat processing functions
def load_n_process():
    filename = input('insert filename of digital twin data: ')

    if filename == '':
        filename = 'database_2.csv'

    df = load_data(filename)
    df = process_string(df)
    make_report(df,filename)
    df = process_relative(df)
    df = process_queues(df)
    df = standardize_pipeline(df)

    return df


# divide the processed data into train and test
def split_data(df, test_percent=0.3):
    # feature columns
    X = df.drop('part_of_interest_rct',axis=1)

    # target column
    y = df['part_of_interest_rct']

    #train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_percent, random_state=72)

    return X_train, X_test, y_train, y_test, X, y


# create models
def create_models():
    model_1 = LinearRegression()
    model_2 = Lasso(alpha=0.5)

    return model_1, model_2


# create predictions considering models
def create_predictons(X_train, y_train, X_test, model_1, model_2):

    model_1.fit(X_train, y_train)
    model_2.fit(X_train, y_train)

    y_pred_1 = model_1.predict(X_test)
    y_pred_2 = model_2.predict(X_test)

    return y_pred_1, y_pred_2


# concat regression functions
def make_regressions(df):
    X_train, X_test, y_train, y_test, X, y = split_data(df)
    model_1, model_2 = create_models()
    y_pred_1, y_pred_2 = create_predictons(X_train, y_train, X_test, model_1, model_2)

    return y_pred_1, y_pred_2, y_test


# evaluate the models performances
def evaluate(y_test, y_pred_1, y_pred_2, print_=True):

    scores = []

    # Evaluation of model 1
    MAE_1 = mean_absolute_error(y_test,y_pred_1)
    RMSE_1 = mean_squared_error(y_test,y_pred_1,squared=False) 
    MSE_1 = mean_squared_error(y_test,y_pred_1) 
    MAPE_1 = np.mean(np.abs((y_test - y_pred_1) / y_test)) * 100

    scores.append((MAE_1, RMSE_1, MSE_1))


    # Evaluation of model 2 
    MAE_2 = mean_absolute_error(y_test,y_pred_2)
    RMSE_2 = mean_squared_error(y_test,y_pred_2,squared=False) 
    MSE_2 = mean_squared_error(y_test,y_pred_2) 
    MAPE_2 = np.mean(np.abs((y_test - y_pred_2) / y_test)) * 100

    scores.append((MAE_2, RMSE_2, MSE_2))

    if print_: 

        print(f"result pipeline 1 (Linear Regression)")
        print(f"Mean Squared Error: {MSE_1}")
        print(f"Root Mean Squared Error: {RMSE_1}")
        print(f"Mean Absolute Error: {MAE_1}")
        print(f"Mean Absolute Percentage Error: {MAPE_1}\n")

        print(f"result pipeline 2 (Lasso)")
        print(f"Mean Squared Error: {MSE_2}")
        print(f"Root Mean Squared Error: {RMSE_2}")
        print(f"Mean Absolute Error: {MAE_2}")
        print(f"Mean Absolute Percentage Error: {MAPE_2}\n")

    return scores


#plot values obtained
def plot_values(y_test,y_pred_1, y_pred_2, save_img=True):
    plt.scatter(y_test, y_pred_1)
    plt.xlabel('True Values')
    plt.ylabel('Predictions_Model_1')
    if save_img:
        plt.savefig('comparasion_model_1.png')
    else:
        plt.show()

    plt.scatter(y_test, y_pred_2)
    plt.xlabel('True Values')
    plt.ylabel('Predictions_Model_2')
    if save_img:
        plt.savefig('comparasion_model_2.png')
    else:
        plt.show()
    
    return None


# get info of df to check for errors
def get_info(df):
    print(df.info())
    print(df.describe().T)

    return None

if __name__ == "__main__":

    df = load_n_process()
    y_pred_1, y_pred_2, y_test = make_regressions(df)
    scores = evaluate(y_test, y_pred_1, y_pred_2)
    plot_values(y_test,y_pred_1, y_pred_2)


    
