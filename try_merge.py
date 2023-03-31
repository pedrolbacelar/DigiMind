import paho.mqtt.client as mqtt
from time import sleep
from main_ML import *
#import libraries
import pandas as pd
import ydata_profiling as pp
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import json
import csv
from random import randrange
from joblib import load
import time
import os
from interface_API import interfaceAPI

#--- variables and flags
localhost = "127.0.0.1"
myip = "192.168.0.50"
RCT_flag = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic = "RCT_request")
    client.subscribe(topic = "stop")


def on_message(client, userdata, msg):
    # define global variables
    global part_id
    global RCT_flag
    print(msg.topic)
    #--- initiate the RCT prediction
    if msg.topic == "RCT_request":
        part_id = str(msg.payload.decode("utf-8"))
        print(f"Requested: RCT for {part_id}")
        RCT_flag = True
    if msg.topic == "stop":
        RCT_flag = False
        print("\33[31mPrediction canceled remotely\33[0m")

#Function that finds the part ID in the Json

def find_id(json_path,part_of_interest_id):
    piece_found = False
    queue_number_to_remaining_machines = {1: 4, 2: 3, 3: 2, 4: 2, 5: 1}
    header = ["queues_initial_conditions", "processing_time_machines", "part_of_interest_current_queue", "part_of_interest_current_position", "remaining_machines", "part_of_interest_rct"]
    with open(json_path,'r') as json_file:
        json_load = json.load(json_file)
    part_of_interest = "Part " + str(part_of_interest_id)
    for index, init in enumerate(json_load['initial']):
        if part_of_interest in init:
            part_of_interest_current_queue = index + 1
            part_of_interest_current_position = init.index(part_of_interest)
            piece_found = True
        else:
            continue
    if piece_found == False:
         return 0,0,0, piece_found
    remaining_machines = queue_number_to_remaining_machines[part_of_interest_current_queue]
    queues_initial_conditions = [len(init) for init in json_load['initial']]
    processing_time_machines = "[11, 17, 60, 38, 10]"
    sample = (queues_initial_conditions, processing_time_machines, part_of_interest_current_queue, part_of_interest_current_position, remaining_machines, 0)
    with open ("test.csv",'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(sample)
    return part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, piece_found

#Preprocessing for the machine learning model
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
def load_n_process(filename, report=True):
    #filename = input('insert filename of digital twin data: ')

    if filename == '':
        filename = 'database_2.csv'

    df = load_data(filename)
    df = process_string(df)
    if report:
        make_report(df,filename)
    df = process_relative(df)
    df = process_queues(df)
    # ALTERED
    df = standardize_pipeline(df)

    return df

# Import the model and predict for a new point
def predict_ML(model,new_point):
    clf = load(model)
    df2 = load_n_process(new_point,report=False)
    df2 = df2.drop('part_of_interest_rct',axis=1)
    y_pred_2 = clf.predict(df2)
    return y_pred_2[0]


def main_ML():
    rct_ML = predict_ML('ml_model.joblib','test.csv')
    return rct_ML


#Function that calls the prediction
def collect_features(json_path,part_of_interest_id):
    #Search for the id_part
    part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, track_part = find_id(json_path,part_of_interest_id)
    # If the piece is found, call the ML model
    if track_part == True:
        rct_ML = main_ML()
        return part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, track_part, rct_ML
    else:
        return part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, track_part, None

client = mqtt.Client()
client.connect(localhost,1883,60) # verify the IP address before connect
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

try:
    while True:
        if RCT_flag == True:
            json_step = 1
            api = interfaceAPI()

            #Call the function for the first json
            json_initial = "./models/initial.json"
            part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, _, rct_ML = collect_features(json_initial,part_of_interest_id)
            #Send this data to the mindsphere
            api.Indicator([0,0.94])
            api.RCT([str(part_of_interest_id),round(rct_ML)])
            api.Zone([part_of_interest_current_queue]+queues_initial_conditions)
            print(part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, rct_ML)

            #Sleep for a specific amount of time
            time.sleep(json_step*3)

            #Count the number of json files minus the first one
            _, _, files = next(os.walk("./models"))
            number_jsons = len(files) - 1

        if RCT_flag == True:
            #iterate for the remaining jsons
            i = 0
            while i < number_jsons and RCT_flag == True:
                check_piece = False
                while check_piece == False and i < number_jsons and RCT_flag == True:
                    # Check all the json files
                    json_path = "./models/" + files[i]
                    part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, check_piece, rct_ML = collect_features(json_path,part_of_interest_id)
                    i += 1
                if check_piece == True:
                    #Send the data to mindsphere
                    print(part_of_interest_current_position, part_of_interest_current_queue, queues_initial_conditions, rct_ML)
                    api.Indicator([0,0.94])
                    api.RCT([str(part_of_interest_id),round(rct_ML)])
                    api.Zone([part_of_interest_current_queue]+queues_initial_conditions)
                time.sleep(json_step*3)
                i += json_step
            RCT_flag = False
except KeyboardInterrupt:
    print("\33[31mML function stopped from keyboard.\33[0m")
    client.publish(topic= 'status', payload = 'ML function stopped from keyboard')
except:
    client.publish(topic= 'status', payload = 'ML function failure')
    print("\33[31mProgram exited inappropriately.\33[0m")
