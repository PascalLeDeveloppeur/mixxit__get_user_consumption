import json
import time
import sys
import datetime

import psycopg2
from psycopg2.extras import Json

from model.metadata import Metadata
from model.log import Log
from constants import (
    ERROR_WHILE_EXECUTING_QUERY,
    SUCCESS_IN_EXECUTING_QUERY,
)


class Dao:
    def __init__(self, config_obj):
        # status_code_of_this_operation SUCCESS_IN_EXECUTING_QUERY=> Succeded, 90=> error while opening connection, ERROR_WHILE_EXECUTING_QUERY=> error while executing query
        self.last_batch_id = None
        self.last_key = None
        self.log = Log()
        self.metadata = Metadata()
        self.connection = None
        self.config = config_obj
        # read connection parameters
        self.cursor = None
        self.params = self.config.config_db()

    def open_db_connection(self):
        is_connection_open = False
        try:
            # connect to the PostgreSQL server
            print("""
Connecting to the PostgreSQL database...""")
            self.connection = psycopg2.connect(**self.params)
            # create a cursor
            self.cursor = self.connection.cursor()
            is_connection_open = True

        except (Exception, psycopg2.DatabaseError) as err:
            is_connection_open = False
            err = str(err)
            if not err:
                err = "Maybe the identifiers are wrong."
            print(f"""Error related to the database
{err}
    """)
            if self.connection is not None:
                self.connection.close()
                print("""Database connection closed.
                    """)
        finally:
            return is_connection_open

    def close_connexion(self):
        try:
            # commit the request (VERY IMPORTANT!!!)
            self.connection.commit()
            # close the communication with the PostgreSQL
            self.cursor.close()
            is_connection_closed = True

        except (Exception, psycopg2.DatabaseError) as err:
            is_connection_closed = False
            err = str(err)
            if not err:
                err = "Unknown error!"
            print(f"""Error related to the database.
Unable to commit the connection or close the cursor
{err}
    """)
        finally:
            if self.connection is not None:
                self.connection.close()
                print("""Database connection closed.
                    """)
            return is_connection_closed

    def check_connection(self, kargs=None):
            """ Connect to the PostgreSQL database server """
            status_code_of_this_operation = SUCCESS_IN_EXECUTING_QUERY

            is_connection_open = self.open_db_connection()

            if is_connection_open:
                try:
                    # execute a statement
                    print("Connection OK!")
                    print('PostgreSQL database version:')
                    self.cursor.execute('SELECT version()')
                    # display the PostgreSQL database server version
                    db_version = self.cursor.fetchone()
                    print(db_version)

                except Exception as err:
                    err = "Error in chek connection: " + str(err)
                    print(err)
                    status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

            else:
                status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

            is_error_when_commit_or_close_cursor = self.close_connexion()

            if is_error_when_commit_or_close_cursor:
                status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY
            response_from_request_dict = {"body": "", "status": status_code_of_this_operation}

    def get_data_usage_by_iccid(self, kargs=None):
        """Connect to the PostgreSQL database server"""
        status_code_of_this_operation = SUCCESS_IN_EXECUTING_QUERY
        is_connection_open = self.open_db_connection()

        if is_connection_open:
            try:
                iccid = kargs["iccid"]
                from_date = kargs["from_date"]
                to_date = kargs["to_date"]

                self.cursor.callproc('get_data_usage_by_iccid', (iccid, from_date, to_date))
                result = self.cursor.fetchall()

            except Exception as err:
                    err = "Error in chek connection: " + str(err)
                    print(err)
                    status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY
        else:
            status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

        is_error_when_commit_or_close_cursor = self.close_connexion()
        if is_error_when_commit_or_close_cursor:
            status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

        return {"body": result, "status": status_code_of_this_operation}

    def get_all_activities_between_dates(self, kargs=None):
        """Get all activities received from WebbingNE"""
        status_code_of_this_operation = SUCCESS_IN_EXECUTING_QUERY
        is_connection_open = self.open_db_connection()

        if is_connection_open:
            try:
                from_date = kargs["from_date"]
                to_date = kargs["to_date"]

                self.cursor.callproc('get_all_activities_between_dates', (from_date, to_date))
                result = self.cursor.fetchall()

            except Exception as err:
                    err = "Error in chek connection: " + str(err)
                    print(err)
                    status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY
        else:
            status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

        is_error_when_commit_or_close_cursor = self.close_connexion()
        if is_error_when_commit_or_close_cursor:
            status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY

        return {"body": result, "status": status_code_of_this_operation}

    def add_to_test(self, kargs):
        the_json, some_text = kargs["my_json"], kargs["my_text"]
        self.cursor.callproc('add_to_test', (the_json, some_text))
        result = self.cursor.fetchone()
        print("id: ", result)

    def log_it(self, kargs=None):
        print()
        print("logging these arguments ...")
        print("is_to_update: ", self.log.is_to_update)
        print("fk_action_status_id: ", self.log.fk_action_status_id)
        print("nbr_of_action_errors: ", self.log.nbr_of_action_errors)
        print("Message: ", self.log.action_msg)
        print("log_datetime_end: ", self.log.log_datetime_end)
        print("fk_status_id: ", self.log.fk_status_id)
        print("is_alert_on: ", self.log.is_alert_on)
        print("fk_batch_id: ", self.log.fk_batch_id)
        print("fk_metadata_id: ", self.log.fk_metadata_id)
        print("fk_download_status_id: ", self.log.fk_download_status_id)
        print("fk_handling_status_id: ", self.log.fk_handling_status_id)
        print()

        is_trying_to_log = True
        nbr_of_log_errors = 0
        while is_trying_to_log:
            if nbr_of_log_errors > 0:
                print()
                print(f"Pause for {RETRY_INTERVAL_IN_SECONDS} seconds before trying again")
                time.sleep(RETRY_INTERVAL_IN_SECONDS)
            try:
                self.cursor.callproc('log_this', (self.log.is_to_update,
                                                self.log.fk_action_status_id,
                                                self.log.nbr_of_action_errors,
                                                self.log.action_msg,
                                                self.log.log_datetime_end,
                                                self.log.fk_status_id,
                                                self.log.is_alert_on,
                                                self.log.fk_batch_id,
                                                self.log.fk_metadata_id,
                                                self.log.fk_download_status_id,
                                                self.log.fk_handling_status_id,))
                result_from_db = self.cursor.fetchone()
                print("result_from_db: ", result_from_db)
                if type(result_from_db[0]) == int:
                    if result_from_db[0] > 0:
                        self.log.fk_status_id = result_from_db[0]
                        is_trying_to_log = False
                    elif result_from_db[0] < 0:
                        raise Exception("Negative response from log.")
                elif result_from_db[0] == None:
                    if nbr_of_log_errors >= 3:
                        raise Exception("To many errors occurred when trying to log the action")
                    raise Exception("No return")
                elif result_from_db[0]:
                    raise Exception(f"The log returned an error #{result_from_db[0]}")
                else:
                    raise Exception(f"An unexpected error has occurred!")
            except Exception as err:
                nbr_of_log_errors +=1
                if nbr_of_log_errors > 3:
                    is_trying_to_log = False
                    err = f"""
**** ALERT!!! ****
To many errors occurred when trying to log the action:
{self.log.action_msg}
""" + str(err)
                    print(err)

                else:
                    err = f"""Error when trying to log: {self.log.action_msg}
""" + str(err)
                print(str(err))

    def log_before_action(self, name_of_action, module_status):
        if module_status == MODULE_STATUS_DICT.get(SUCCESS_IN_EXECUTING_QUERY):
            # preparing data to be logged:
            self.log.action_msg = name_of_action
            self.log.is_to_update = False
            self.log.fk_action_status_id = 1
            self.log.fk_batch_id = self.last_batch_id
            self.log.log_datetime_end = None
            print()
            print(f"Is creating log before this action: {name_of_action}")

            # request for log ****
            self.open_close_db_connection(self.log_it)

    def log_after_action(self, name_of_action, result_status):
        print()
        print(f"Is creating log after: {name_of_action}")
        # preparing data to be logged:
        self.log.log_datetime_end = datetime.datetime.now()
        self.log.action_msg = name_of_action
        self.log.is_to_update = True

        if result_status == SUCCESS_IN_EXECUTING_QUERY:  # action succeded
            self.log.fk_action_status_id = 2
        else:  # action to be retried
                self.log.fk_action_status_id = 3
        if result_status != 10:
            print("nbr of action erors: ", self.log.nbr_of_action_errors)

        # action failed
        if self.log.nbr_of_action_errors >= MAX_SUBMODULE_ERRORS:
            if result_status == 10:
                self.log.nbr_of_action_errors = 0
                self.log.fk_action_status_id = 5
            else:
                self.log.fk_action_status_id = 4

        # request for log ****
        self.open_close_db_connection(self.log_it)
        if result_status == 10:
            self.log.nbr_of_action_errors = 9999999

    def batch_it(self, kargs=None):
        this_method_name = "batch it"
        sql_function_name = "batch_this"
        status_code_if_error = 94
        batch_in_json = Json(kargs[0])
        kargs[0] = batch_in_json
        response = self.execute_sql_function_the_return_of_which_is_nbr(this_method_name, sql_function_name, kargs, status_code_if_error)
        return response

    def get_last_key(self, kargs=None):
        status_code_of_this_operation = SUCCESS_IN_EXECUTING_QUERY
        print("Executing: Get last key")
        try:
            self.cursor.callproc('get_last_key')
            # import ipdb; ipdb.set_trace()
            try:
                self.last_key = self.cursor.fetchone()[0]
            except:
                self.last_key = ""
            if type(self.last_key) != str:
                raise Exception("The answer should have been an string but it is not!")
            return {"body": self.last_key, "status": status_code_of_this_operation}
        except Exception as err:
            err = "Error in get last key: " + str(err)
            print(err)
            status_code_of_this_operation = ERROR_WHILE_EXECUTING_QUERY
            return {"body": None, "status": status_code_of_this_operation}

    def store_metadata(self, kargs=None):
        this_method_name = "Store metadata"
        sql_function_name = "store_metadata"
        status_code_if_error = 93
        response = self.execute_sql_function_the_return_of_which_is_nbr(this_method_name, sql_function_name, kargs, status_code_if_error)
        return response

    def push_csv_data_to_db(self,kargs=None):
        this_method_name = "push csv data to db"
        sql_function_name = "push_csv_data_to_db"
        status_code_if_error = 92
        response = self.execute_sql_function_the_return_of_which_is_nbr(this_method_name, sql_function_name, kargs, status_code_if_error)
        return response

    def execute_sql_function_the_return_of_which_is_nbr(self, this_method_name, sql_function_name, kargs, status_code_if_error):
        status_code_of_this_operation = SUCCESS_IN_EXECUTING_QUERY
        print(f"Executing: {this_method_name}")
        try:
            # self.cursor.callproc('batch_this',"This results in an error") #  <= pour déclencher une erreur
            self.cursor.callproc(sql_function_name, kargs)
            response_from_db = self.cursor.fetchone()
            print(f"response_from_db: {response_from_db}")
            if not response_from_db:
                raise Exception("No response from query to database")
            if type(response_from_db[0]) == int:
                if response_from_db[0] < 0:
                    raise Exception("Probably argument error in the query to database")
            else:
                raise Exception("The answer should have been an integer but it is not!")
            return {"body": response_from_db, "status": status_code_of_this_operation}
        except Exception as err:
            err = f"Error in: {this_method_name}: " + str(err)
            print(err)
            status_code_of_this_operation = status_code_if_error
            return {"body": 0, "status": status_code_of_this_operation}
