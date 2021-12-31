import pandas as pd
import json
import mongodb
import logger
import preprocessing
from sklearn.preprocessing import StandardScaler
from pickle import dump

mongodb = mongodb.MongoDBOperation()
log = logger.Logging("Transformation")


class Transformation:
    def __init__(self):
        self.preprocessing = preprocessing.Preprocessing()
        with open("data_config.json", "r") as file:
            self.transform = json.load(file)
        self.transform = self.transform["datatype_transform_columns"]
        self.scale = StandardScaler()

    def convert_col_float(self):
        try:
            self.preprocessing.unite_dataset()
            df = mongodb.get_dataframe_of_collection(db_name="Training", collection_name="dataset")
            for col in self.transform["float"]:
                if col == "cost":
                    df[col] = df[col].astype(str)
                    df[col] = df[col].apply(lambda x: x.replace(",", ""))
                    df[col] = df[col].astype(float)
                elif col == "rate":
                    df = df.loc[df[col] != "NEW"]
                    df = df.loc[df[col] != "-"]
                    df[col] = df[col].astype(str)
                    df[col] = df[col].apply(lambda x: x[:-2].strip())
                    df[col] = df[col].astype(float)
                    break
            df = self.transforming_col(df)  # Transforming columns
            return df
            log.log("Converting column to type Float")
        except Exception as e:
            log.log("Error while converting columns to float type")

    def reduce_data_from_column(self, column):
        '''
        column:rest_type column has many values. Since they are comma separated,
        we will pick the first information before
        comma.
        :return:a single value before comma
        Example:
        "Cafe, Casual Dining, Bar"
        This function will return "Cafe"
        '''
        try:
            if ',' in column:
                return column[:column.find(",")]
            else:
                return column
        except Exception as e:
            log.log("Error in reducing data from column")

    def sorting(self, column):
        try:
            column = column.split(", ")  # converting to list
            sort = sorted(column)  # sorting
            return ', '.join(sort)  # return a string of sorted values
        except Exception as e:
            log.log(f'Error in Sorting column:{column}')
            raise (e)

    def length(self, column):
        try:
            return len((column.split(", ")))
        except Exception as e:
            log.log(f"Error in return length")

    def transforming_col(self, df):
        try:
            column_names = ['rest_type', 'cuisines', 'dish_liked']
            df[column_names[0]] = df[column_names[0]].apply(self.reduce_data_from_column)
            df[column_names[1]] = df[column_names[1]].apply(self.sorting)
            df[column_names[2]] = df[column_names[2]].apply(self.length)
            log.log(f"Transforming columns {column_names}")
            return df
        except Exception as e:
            log.log(f"Error in transforming Columns: {column_names}")
            raise(e)

    def drop_duplicates(self, df):
        try:
            df.drop_duplicates(inplace=True)
            log.log("Dropping Duplicates")
            return df
        except Exception as e:
            print(str(e))

    def encoding(self):
        try:
            df = self.convert_col_float()
            columns_encode = df.select_dtypes(include=["object"]).columns.to_list()
            df = self.drop_duplicates(df)
            df.reset_index(inplace=True, drop=True)
            for columns in columns_encode:
                data = dict()
                count = 1

                for val in df[columns].unique():
                    data[val] = count
                    count += 1
                if mongodb.drop_collection(db_name='Training', collection_name=columns):
                    mongodb.insert_record_in_collection(db_name="Training", collection_name=columns, record=data)
                df[columns] = df[columns].map(data)
            log.log("Encoding categorical variable and saving it to Mongodb")
            return df
        except Exception as e:
            log.log("Error in encoding")
            raise(e)

    def data_scaling(self):
        try:
            df = self.encoding()
            x = df.drop(columns=['rate'])
            scaler = self.scale.fit(x)
            scaled_data = self.scale.fit_transform(x)
            dump(self.scale, open("scaler.pkl", "wb"))
            columns = x.columns.tolist()
            scaled_df = pd.DataFrame(scaled_data, columns=columns)
            scaled_df['rate'] = df['rate']
            scaled_df.to_csv("master.csv")
            return scaled_df
        except Exception as e:
            log.log("Error in Data Scaling")
            raise(str(e))


if __name__=="__main__":
    test = Transformation()
    test.data_scaling()