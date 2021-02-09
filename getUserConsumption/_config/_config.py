from os import path, sys, getenv, getcwd
import time
from configparser import ConfigParser

from dotenv import load_dotenv

from constants import COMMAND_LINE_EXAMPLE


class Config:

    def __init__(self):
        self.__environment = None
        self.__launched_file = None
        self.__function_to_execute = None
        self.__args_from_command_line = None
        self.MAIN_ROOT = getcwd()
        self.__config_dotenv()

    def get_function_to_execute(self):
        return self.__function_to_execute

    def get_args_from_command_line(self):
        return self.__args_from_command_line

    def __config_dotenv(self):

        """.env creator

        len(sys.argv) = 1 if the app is launched like the following:
              python3 myfile.py
        len(sys.argv) = 2 if the app is launched like the following:
              python3 myfile.py dev
              (dev means development
               prod => production; perso => personal; pascal => pascal)"""
        command_line = []
        for one_arg in sys.argv:
            command_line.append(one_arg.lower())

        self.parse_commande_line(command_line)

        if self.__environment == "pascal":
            # Copy .env_pascal to create .env
            try:
                with open(path.join(self.MAIN_ROOT, ".env_pascal"), "r",
                            encoding="utf-8") as env_file:
                    env_content = env_file.read()

                with open(path.join(self.MAIN_ROOT, ".env"), "w",
                            encoding="utf-8") as env_file:
                    env_file.write(env_content)
            except Exception as err:
                err = """
Error during the creation of the .env file.
""" + str(err)
                print(err)

        if self.__environment == "prod":
            # Copy .env_prod to create .env
            try:
                with open(path.join(self.MAIN_ROOT, ".env_prod"), "r",
                            encoding="utf-8") as env_file:
                    env_content = env_file.read()

                with open(path.join(self.MAIN_ROOT, ".env"), "w",
                            encoding="utf-8") as env_file:
                    env_file.write(env_content)
            except Exception as err:
                err = """
Error during the creation of the .env file.
""" + str(err)
                print(err)

        if self.__environment == "dev":
            # Copy .env_dev to create .env
            try:
                with open(path.join(self.MAIN_ROOT, ".env_dev"), "r",
                            encoding="utf-8") as env_file:
                    env_content = env_file.read()

                with open(path.join(self.MAIN_ROOT, ".env"), "w",
                            encoding="utf-8") as env_file:
                    env_file.write(env_content)
            except Exception as err:
                err = """
Error during the creation of the .env file.
""" + str(err)
                print(err)

        if not self.__environment:
            print("Error! Environment is not specified")
            print("You need to type a command line instruction as follows:")
            print(COMMAND_LINE_EXAMPLE)
            sys.exit()

        print("")
        print("**************************")
        print("Environment : ", self.__environment)
        print("")

        time.sleep(3) # Wait for the .env file creation
        load_dotenv() # load the .env file


    def config_db(self, filename=path.join(
            "getUserConsumption", "_config", "_database.ini"),
                    section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
            db["password"] = getenv("db_password")
        else:
            raise Exception(f'Section {section} not found in the {filename} file')

        return db

    def parse_commande_line(self, command_line):
        if len(command_line) > 1:
            self.__launched_file,\
                self.__function_to_execute,\
                *self.__args_from_command_line,\
                self.__environment\
                = command_line
            if self.__environment != "prod"\
                    and self.__environment != "dev"\
                    and self.__environment != "pascal":
                self.__environment = None
        else:
            self.__environment = None
