from pymongo import MongoClient
import datetime
import mysql.connector
import pytz
import uuid


class refactorUnavilable:
    def __init__(self,tenant, TENANT, mongo_link):
        self.client = MongoClient(mongo_link)
        self.db = self.client[f"{tenant}-app-testing"]
        self.collection = self.db[f"{tenant}-test-devices"]
        self.TENANT = TENANT
        self.mongo_link = mongo_link

    def create_db(self, cursor, create_db_query, check_table_query, create_table_query, database, table, use_db_query):
        cursor.execute(create_db_query)
        cursor.execute(use_db_query)
        # cursor.execute(check_table_query)
        self.create_collection(cursor, check_table_query, create_table_query, table)
        print(f"db created with name {database}")

    def create_collection(self, cursor, check_table_query, create_table_query, table):
        cursor.execute(check_table_query)
        if cursor.fetchone():
            # Table exists, do not create it again
            print(f"Table already exists with name of {table}.")
        else:
            cursor.execute(create_table_query)
            print(f"Table created successfully with the name of {table}")

    def check_db_table(self, host, user, password, check_db_query, use_db_query, database, check_table_query,
                       create_table_query,table, create_db_query):
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = cnx.cursor()
        cursor.execute(check_db_query)

        if cursor.fetchone():
            cursor.execute(use_db_query)
            print(f"db already present with the name of {database}")
            self.create_collection(cursor, check_table_query, create_table_query, table)
            print("start inserting")
        else:

            self.create_db(cursor, create_db_query, check_table_query, create_table_query, database, table, use_db_query)
        cnx.commit()
        cursor.close()
        cnx.close()

    def connect_insert(self, host, user, password, database, check_query, insert_query, update_query, data):
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = cnx.cursor()

        for row in data:
            cursor.execute(insert_query, row)
                # print("data....",update_query, row)

        cnx.commit()
        # print(f"{cursor.rowcount} rows inserted or updated.")
        cursor.close()
        cnx.close()


    def create_data(self):
        query = {'deviceParameters.deviceStatus': 'unavailable'}
        results = self.collection.find(query)
        return list(results)

    def get_all_data(self):
        results = self.collection.find()
        return list(results)

    def send_sql(self, host, user, password, database, check_query, insert_query, update_query):
        docs = self.get_all_data()
        for doc in docs:
            now = datetime.datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            new_timestamp = now.astimezone(ist)

            # dict_data = {
            #     "deviceid": doc["serial"],
            #     "devicename": doc["modelName"],
            #     "status": "up",
            #     "timestamp": new_timestamp,
            #     "platform" : doc["platform"]
            # }
            # if doc["deviceParameters"]["deviceStatus"] == "unavailable":
            #     dict_data["status"] = "down"

            dict_data = {
                        "deviceid": doc.get("serial", "unknown"),
                        "devicename": doc.get("modelName", "unknown"),
                        "status": "up",
                        "timestamp": new_timestamp,
                        "platform": doc.get("platform", "unknown")
                    }
            
            try:
                if doc["deviceParameters"]["deviceStatus"] == "unavailable":
                    dict_data["status"] = "down"
            except KeyError:
                # print("101: ", doc.get("serial", "unknown"))
                print("Skipping doc due to missing 'deviceStatus' key.")
                continue  # Skip the current iteration
            # if doc["deviceParameters"]["deviceStatus"] == "unavailable":
            #     dict_data["status"] = "down"

            if dict_data["platform"] == "android":
                dict_data["platform"] = "Android"
            if dict_data["platform"] == "ios":
                dict_data["platform"] = "iOS"
            if dict_data["platform"] == "tv":
                dict_data["platform"] = "TV"

            new_uuid = str(uuid.uuid4())
            # if doc["version"] == "1.0":
            #     dict_data["city"] = doc["deviceParameters"]["city"]
            #     data = [(new_uuid, dict_data["devicename"], dict_data["deviceid"], dict_data["status"], dict_data["timestamp"], dict_data["platform"], dict_data["city"])]
            #     # data = [(dict_data["devicename"], dict_data["deviceid"],dict_data["status"], datetime.datetime.now())]
            # else:
            #     dict_data["city"] = doc["controllerParameters"]["city"]
            #     data = [(new_uuid, dict_data["devicename"], dict_data["deviceid"], dict_data["status"], dict_data["timestamp"], dict_data["platform"], dict_data["city"])]

            if "deviceParameters" in doc and "city" in doc["deviceParameters"]:
                dict_data["city"] = doc["deviceParameters"]["city"]
                data = [(new_uuid, dict_data["devicename"], dict_data["deviceid"], dict_data["status"], dict_data["timestamp"], dict_data["platform"], dict_data["city"])]
                # data = [(dict_data["devicename"], dict_data["deviceid"],dict_data["status"], datetime.datetime.now())]
            else:
                dict_data["city"] = doc["controllerParameters"]["city"]
                data = [(new_uuid, dict_data["devicename"], dict_data["deviceid"], dict_data["status"], dict_data["timestamp"], dict_data["platform"], dict_data["city"])]


            self.connect_insert(host, user, password, database, check_query, insert_query, update_query, data)

    def datetime_format(self):
        current_datetime = datetime.datetime.now()
        ist_datetime = current_datetime.strftime("%d/%m/%Y %H:%M IST")
        return ist_datetime


