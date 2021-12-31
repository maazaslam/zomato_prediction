import pymongo
import json
import pandas as pd
import logger

log = logger.Logging("Database")

class MongoDBOperation:
    def __init__(self):
        pass

    def get_mongo_db_url(self, url=None):
        """
        :return: mongo_db_url
        """
        try:
            if url is None:
                url = "localhost:27017/"
            return url
        except Exception as e:
            mongo_db_exception = "Failed to connect"
            log.log("Error in get_mongo_db_url")
            raise Exception(mongo_db_exception) from e

    def get_database_client_object(self):
        """
        Return pymongoClient object to perform action with MongoDB
        """
        try:
            client = pymongo.MongoClient(f'mongodb://{self.get_mongo_db_url()}')  # creating database client object
            return client
        except Exception as e:
            mongo_db_exception ="Failed to fetch  data base client object."
            raise Exception(mongo_db_exception) from e

    def close_database_client_object(self, obj_name):
        """


        Parameters
        ----------
        obj_name : pymongo client
            DESCRIPTION.pymongo client object

        Raises
        ------
        Exception
            Failed to close database connection-->.

        Returns
        -------
        bool
            True if connection closed.

        """
        try:
            obj_name.close()
            return True
        except Exception as e:
            mongo_db_exception = "Failed to close data base client"
            raise Exception(mongo_db_exception) from e

    def is_database_present(self, client, db_name):
        """

        Parameters
        ----------
        client : pymongo client
            DESCRIPTION. object which will be used to fetch communicate with mongo db
        db_name : string
            database name.

        Raises
        ------
        Exception
            DESCRIPTION.If any exception occurs

        Returns
        -------
        bool
            True if database already exists.

        """
        try:
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            mongo_db_exception = "Failed during checking database."
            raise Exception(mongo_db_exception) from e

    def create_database(self, client, db_name):
        """
        client: client object of database
        db_name:data base name
        """
        try:
            return client[db_name]
        except Exception as e:
            mongo_db_exception = "Failure occurred during database creation steps"
            raise Exception(mongo_db_exception) from e

    def create_collection_in_database(self, database, collection_name):
        """
        database:database
        collection_name: name of collection
        return:
            collection object
        """
        try:
            return database[collection_name]
        except Exception as e:
            mongo_db_exception = "Failed during creating collection in database"
            raise Exception(mongo_db_exception) from e

    def is_collection_present(self, collection_name, database):
        """


        Parameters
        ----------
        collection_name : collection_name
            DESCRIPTION.collection name which needs to verify
        database : TYPE
            DESCRIPTION.database in which collection needs to check for existence

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        bool
            true if collection present in database.

        """
        try:
            """It verifies the existence of collection name in a database"""
            collection_list = database.list_collection_names()

            if collection_name in collection_list:
                # print("Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' exists")
                return True

            # print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' does not exists OR \n        no documents are present in the collection")
            return False
        except Exception as e:
            mongo_db_exception = "Failed during checking collection"
            raise Exception(mongo_db_exception) from e

    def get_collection(self, collection_name, database):
        """
        collection_name:collection name
        database=database
        ------------------------------------------
        return collection object
        """
        try:
            client = self.get_database_client_object()
            database = database
            collection = self.create_collection_in_database(database, collection_name)
            return collection
        except Exception as e:
            mongo_db_exception = "Failed in retrieval of collection"
            raise Exception(mongo_db_exception) from e

    def is_record_present(self, db_name, collection_name, record):
        """
        db_name: database name
        collection_name: collection name
        record: records to search
        ----------------------------------------------
        return True if record exists else return false
        """
        try:
            client = self.get_database_client_object()  # client object
            database = self.create_database(client, db_name)  # database object
            collection = self.get_collection(collection_name, database)  # collection object
            record_found = collection.find(record)  # fetching record
            if record_found.count() > 0:
                client.close()
                return True
            else:
                client.close()
                return False
        except Exception as e:
            mongo_db_exception = "Failed in fetching record"
            raise Exception(mongo_db_exception) from e

    def create_record(self,collection, data):
        """
        collection: Accept collection name
        data: accept single to insert into collection
        -------------------------------------------
        return 1 if record inserted
        """
        try:
            collection.insert_one(data)  # insertion of record in collection
            return 1
        except Exception as e:
            mongo_db_exception = "Failed in inserting record"
            raise Exception(mongo_db_exception) from e

    def create_records(self, collection, data):
        """
        collection: collection object
        data: data which needs to be inserted
        --------------------------------------------
        return no of record inserted
        """
        try:
            collection.insert_many(data)
            return len(data)
        except Exception as e:
            mongo_db_exception = "Failed in inserting records"
            raise Exception(mongo_db_exception) from e

    def insert_record_in_collection(self, db_name, collection_name, record):
        """
        db_name: database name
        collection_name: collection name
        record: records to insert
        ------------------------------
        return No of record inserted(int).
        """
        try:
            no_of_row_inserted = 0
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.get_collection(collection_name, database)
            try:
                if not self.is_record_present(db_name, collection_name, record):
                    no_of_row_inserted = self.create_record(collection=collection, data=record)
            except:
                no_of_row_inserted = self.create_record(collection=collection, data=record)
            return no_of_row_inserted
        except Exception as e:
            mongo_db_exception = "Failed in inserting record  in collection"
            raise Exception(mongo_db_exception) from e

    def drop_collection(self, db_name, collection_name):
        """

        :param db_name: database name
        :param collection_name:  collection name
        :return: True if collection droped successfully.
        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            if self.is_collection_present(collection_name, database):
                collection_name = self.get_collection(collection_name, database)
                collection_name.drop()
                return True
        except Exception as e:
            mongo_db_exception = "Failed in dropping collection"
            raise Exception(mongo_db_exception) from e

    def insert_records_in_collection(self, db_name, collection_name, records):
        """
        db_name: database name
        collection_name: collection name
        records: records to insert
        """
        try:
            no_of_row_inserted = 0
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.get_collection(collection_name, database)
            for record in records:
                if not self.is_record_present(db_name, collection_name, record):
                    no_of_row_inserted = no_of_row_inserted + self.create_record(collection=collection, data=records)
            client.close()
            return no_of_row_inserted
        except Exception as e:
            mongo_db_exception = "Failed in inserting records"
            raise Exception(mongo_db_exception) from e

    def insert_dataframe_into_collection(self, db_name, collection_name, data_frame):
        """
        db_name:Database Name
        collection_name: collection name
        data_frame: dataframe which needs to be inserted
        return:

        """
        try:
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.get_collection(collection_name, database)
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            mongo_db_exception = "Failed in inserting dataframe in collection"
            raise Exception(mongo_db_exception) from e

    def get_record(self, database_name, collection_name, query=None):
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, database_name)
            collection = database[collection_name]
            record = collection.find_one(query)
            return record
        except Exception as e:
            mongo_db_exception = "Failed in retrieving record in collection"
            raise Exception(mongo_db_exception) from e

    def get_min_value_of_column(self, database_name, collection_name, query, column):
        """

        :param database_name:
        :param collection_name:
        :param query: to get all record
        :param column: column name
        :return: minimum value
        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, database_name)
            collection = self.get_collection(collection_name=collection_name, database=database)
            min_value = collection.find(query).sort(column, pymongo.ASCENDING).limit(1)
            value = [min_val for min_val in min_value]
            if len(value) > 0:
                if column in value[0]:
                    return value[0][column]
                else:
                    return None
            else:
                return None
        except Exception as e:
            mongo_db_exception = "Failed in getting minimum value from column in collection"
            raise Exception(mongo_db_exception) from e

    def get_max_value_of_column(self, database_name, collection_name, query, column):
        """

        :param database_name: database name
        :param collection_name: collection name
        :param query: query
        :param column: column name
        :return: maximum value
        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, database_name)
            collection = self.get_collection(collection_name=collection_name, database=database)
            max_value = collection.find(query).sort(column, pymongo.DESCENDING).limit(1)
            value = [max_val for max_val in max_value]
            if len(value) > 0:
                if column in value[0]:
                    return value[0][column]
                else:
                    return None
            else:
                return None

        except Exception as e:
            mongo_db_exception = "Failed in getting maximum value from column"
            raise Exception(mongo_db_exception) from e

    def get_records(self, database_name, collection_name, query=None):
        """

        :param database_name:
        :param collection_name:
        :param query:
        :return: cursor object you need to iterate
        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, database_name)
            collection = database[collection_name]
            record = collection.find(query, {'_id': False})
            for info in record:
                data = info
            return data
        except Exception as e:
            mongo_db_exception = "Failed in retrieving records in collection"
            raise Exception(mongo_db_exception) from e

    def update_record_in_collection(self, database_name, collection_name, query, new_value):
        """

        :param database_name: database name
        :param collection_name: collection name
        :param query: search for record
        :param new_value: updated values
        :return: n_updated row
        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, database_name)
            collection = self.get_collection(collection_name=collection_name, database=database)
            update_query = {'$set': new_value}
            result = collection.update_one(query, update_query)
            client.close()
            return result.raw_result["nModified"]
        except Exception as e:
            mongo_db_exception = "Failed updating record in collection"
            raise Exception(mongo_db_exception) from e

    def get_dataframe_of_collection(self, db_name, collection_name, query=None):
        """

        Parameters
        ----------
        db_name : string
            DESCRIPTION. database name
        collection_name : string
            DESCRIPTION.collection name

        Returns
        -------
        Pandas data frame of  collection name present database.

        """
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.get_collection(collection_name=collection_name, database=database)
            if query is None:
                query = {}
            df = pd.DataFrame(list(collection.find(query)))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            return df.copy()
        except Exception as e:
            mongo_db_exception = "Failed in returning dataframe of collection"
            raise Exception(mongo_db_exception) from e

    def remove_record(self, db_name, collection_name, query):
        try:
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.get_collection(collection_name=collection_name, database=database)
            collection.delete_one(query)
            return True
        except Exception as e:
            log.log("Error in removing record")
            raise e

    def collection_names(self, db_name):
        try:
            client = self.get_database_client_object()
            mydb = client[db_name]
            coll_names = [coll_names for coll_names in mydb.list_collection_names()]
            log.log(f"Getting collection names in {db_name.upper()}")
            return coll_names
        except Exception as e:
            log.log(f"Error in getting collection names method")
            raise(e)