import json
import os


def loadConfig():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open("config.json") as inFile:
        config = json.load(inFile)
    return config


class Config:
    config = loadConfig()

    # Certificate
    CRT_FILE = config["CRT_FILE"]
    CRT_KEY = config["CRT_KEY"]

    # Database
    DB_HOST = config["DB_HOST"]
    DB_USER = config["DB_USER"]
    DB_PASS = config["DB_PASS"]
    DB_NAME = config["DB_NAME"]

    # Server
    PORT = config["PORT"]
    DEBUG = config["DEBUG"]
    SSH_PW = config["SSH_PW"]
