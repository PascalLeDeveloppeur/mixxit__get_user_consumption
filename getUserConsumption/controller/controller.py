from _config._config import Config
from EEAL.DAO import Dao
from constants import (
    GET_USER_CONSUMPTION,
    GET_ALL_ACTIVITIES_BETWEEN_DATES)

class Controller:

    def __init__(self):
        self.__config = Config()
        self.__dao = Dao(self.__config)

    def get_config(self):
        return self.__config

    def get_dao(self):
        return self.__dao

    def run(self):
        self.__dao.check_connection()
        function_to_execute = self.__config.get_function_to_execute()

        if self.do_args_conform_to_function(function_to_execute):
            args = self.__config.get_args_from_command_line()
            kargs = {}

            if function_to_execute == GET_USER_CONSUMPTION:
                kargs['iccid'] = args[0][6:]
                kargs['from_date'] = args[1][5:]
                kargs['to_date'] = args[2][3:]
                self.get_user_consumption_by_iccid(**kargs)

            if function_to_execute == GET_ALL_ACTIVITIES_BETWEEN_DATES:
                kargs['from_date'] = args[0][5:]
                kargs['to_date'] = args[1][3:]
                self.get_all_activities_between_dates(**kargs)

        else:
            print("Request from cli not conform")

        print("End of operation")

    def get_user_consumption_by_iccid(self, iccid, from_date, to_date):
        kargs = {"iccid": iccid,
                 "from_date": from_date,
                 "to_date": to_date}
        response_dict = self.__dao.get_data_usage_by_iccid(kargs)
        result = response_dict["body"]
        for row in result:
            print("__________________________")
            print("CONSUMPTION")
            print(f"Upload: {row[0]} octets")
            print(f"Download: {row[1]} octets")
            print(f"Sum: {row[0] + row[1]}")
            print("__________________________")
            print()

    def get_all_activities_between_dates(self, from_date, to_date):
        kargs = {"from_date": from_date,
                 "to_date": to_date}
        response_dict = self.__dao.get_all_activities_between_dates(kargs)
        result = response_dict["body"]

        print()
        print("__________________________")
        print("ALL ACTIVITIES")
        for row in result:
            print(row)
        print("__________________________")
        print()

    def do_args_conform_to_function(self, function_to_execute):
        print("Action to execute: ", function_to_execute)
        do_conform = False
        args = self.__config.get_args_from_command_line()

        if function_to_execute == GET_USER_CONSUMPTION and len(args) == 3:
            print("args[0]: ", args[0])
            print("args[1]: ", args[1])
            print("args[2]: ", args[2])
            if args[0].startswith("iccid:")\
                    and args[1].startswith("from:")\
                    and args[2].startswith("to:"):
                do_conform = True

        if function_to_execute == GET_ALL_ACTIVITIES_BETWEEN_DATES and len(args) == 2:
            print("args[0]: ", args[0])
            print("args[1]: ", args[1])
            if args[0].startswith("from:")\
                    and args[1].startswith("to:"):
                do_conform = True

        return do_conform
