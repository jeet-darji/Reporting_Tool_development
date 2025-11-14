import json
from pymongo import MongoClient
from utilities.aws_secret_trial import AWSSecretManager 
from configuration.constants import (
    MONGO_CONNECTION_STRING,
    MAPPING_DATABASE_NAME,
    MONGO_CONNECTION_STRING,
    SECRETS_MANAGER_MONGO_KEY_NAME_FORMAT,
    MONGO_CONNECTION_STRING_TENANT_WISE
)


from configuration.Logger import Logger

logger = Logger().get_logger(__name__)

# here we need to pass mongo_URI
class DatabaseConnector:

    def __init__(self): # pass URI here
        self.client = MongoClient(MONGO_CONNECTION_STRING)
        self.database_instance = self.client[MAPPING_DATABASE_NAME]   