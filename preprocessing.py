import mongodb
import logger
import pandas as pd
import os
import json

mongodb = mongodb.MongoDBOperation()
log = logger.Logging("Preprocessing")
db_name = "Training"


class Preprocessing:
    def __init__(self):
        self.file_loc = 'Data'

    def unite_dataset(self):
        try:
            log.log("Uniting the Dataset")
            df = pd.DataFrame()
            for file in os.listdir(self.file_loc):
                df_temp = pd.read_csv(f'{self.file_loc}/{file}')
                df = pd.concat([df, df_temp])
            df = self.handle_null(df)  # Handle Null values
            df = self.drop_columns(df)  # Removing unnecessary columns
            df = self.change_column_names(df) #Changing column names
            # if mongodb.drop_collection(db_name=db_name, collection_name="dataset"):
            #     mongodb.insert_dataframe_into_collection(db_name="Training", collection_name="dataset", data_frame=df)
            if "dataset" not in mongodb.collection_names("Training"):
                mongodb.insert_dataframe_into_collection(db_name="Training", collection_name="dataset", data_frame=df)
            return None
        except Exception as e:
            log.log("Error in uniting dataset")
            raise(e)

    def handle_null(self, df):
        try:
            df = df.dropna()
            log.log("Dropping Null values")
            return df
        except Exception as e:
            log.log("Error while dropping null values")
            raise(e)

    def drop_columns(self, df):
        try:
            log.log("Dropping Columns")
            with open("data_config.json", 'r') as file:
                columns_names = json.load(file)
            columns_names = columns_names["Preprocessing"]
            df = df.drop(columns=columns_names["unnecessarycolumns"], axis=1)
            return df
        except Exception as e:
            log.log("Error while dropping unnecessary columns")
            raise(e)

    def change_column_names(self, df):
        try:
            with open("data_config.json", "r") as file:
                change_col_names = json.load(file)
            change_col_names = change_col_names["change_col_names"]
            df = df.rename(columns=change_col_names)
            log.log("Change column names")
            return df
        except Exception as e:
            log.log("Error in change_column_name")
            raise(e)