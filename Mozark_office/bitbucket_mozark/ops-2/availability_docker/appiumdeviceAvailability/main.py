import datetime
import pytz
from appiumdevice_availibility import appiumUnavilable



india_timezone = pytz.timezone('Asia/Kolkata')
exclude_start_time = datetime.time(10, 0)
exclude_end_time = datetime.time(14, 0)

now = datetime.datetime.now(india_timezone)


# webhook_link = "https://mozark.webhook.office.com/webhookb2/df0b711c-085c-4546-8c5c-5d42c5b4580e@e0f7d4ce-7acf-4227-941b-3216dc5bbde9/IncomingWebhook/c096e653ec3443f3bf8c870652f6541c/4a53a2f6-bdec-49a1-9b36-a425bb52a3cc"
# tenant = 'spn'
# TENANT = 'SPN'

tenant = 'icici'
TENANT = 'ICICI'

query = {"deviceParameters.appiumUrl": {"$exists": True}, "serial": {"$ne": "00008020-00123D400CB8002E"}}
mongo_link = "mongodb+srv://mozark-mongo:9bZu8T5ZHMy3Vn1R@cluster0.dlbyh.mongodb.net/event-data?authSource=admin" \
             "&replicaSet=atlas-yjhvlo-shard-0&readPreference=primary&ssl=true"


sql_host = "automation-dashboard-mysql-rds.chgg9hhqherh.ap-south-1.rds.amazonaws.com"
sql_user = "mozarkadmin"
sql_password = "Mozark##2023"

# sql_host = "localhost"
# sql_user = "root"
# sql_password = "Rutvi@2021"

sql_database = f"{tenant}_analytics"
sql_table = "appium_device_availability"


check_db_query = f"SHOW DATABASES LIKE '{sql_database}'"
create_db_query = f"create database {sql_database}"
use_db_query = f"use {sql_database}"

create_table_query = f"CREATE TABLE {sql_table} (uuid VARCHAR(45) PRIMARY KEY, device_name VARCHAR(45), device_serial VARCHAR(45), device_status VARCHAR(45), time_stamp DATETIME, device_platform VARCHAR(45), device_city VARCHAR(45), appium_port VARCHAR(45), wda_port VARCHAR(45), controller_id VARCHAR(45), appium_url VARCHAR(45))"

check_table_query = f"SHOW TABLES LIKE '{sql_table}'"
insert_query = f"insert into {sql_table} (uuid, device_name, device_serial, device_status , time_stamp, device_platform, device_city, appium_port, wda_port, controller_id, appium_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


if now.weekday() == 5 and exclude_start_time <= now.time() <= exclude_end_time:
    print("Script execution is excluded on Saturdays between 10 AM and 2 PM.")
else:
    deviceunavailable = appiumUnavilable(tenant, TENANT, mongo_link)
    results_list = deviceunavailable.create_data(query)
    deviceunavailable.check_db_table(sql_host, sql_user, sql_password, check_db_query, use_db_query, sql_database,
                                    check_table_query, create_table_query, sql_table, create_db_query)

    deviceunavailable.send_sql(sql_host, sql_user, sql_password, sql_database,insert_query, results_list)
    # print("Added in existing table")
