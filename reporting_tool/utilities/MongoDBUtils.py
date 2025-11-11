import json
import pymongo
import os
from pymongo import MongoClient

from configuration.constants import (
    MONGO_CONNECTION_STRING,
    MAPPING_DATABASE_NAME,
    MONGO_CONNECTION_STRING
    # SECRETS_MANAGER_MONGO_KEY_NAME_FORMAT
)


from configuration.Logger import Logger

logger = Logger().get_logger(__name__)


class DatabaseConnector:

    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_STRING)
        self.database_instance = self.client[MAPPING_DATABASE_NAME]

    # -------------------------------------------------------
    # PREPARE CONNECTION STRING
    # -------------------------------------------------------
    # def prepare_connection_string(self, secret_string: dict):
    #     validator = JsonRequestValidator()

    #     if validator.validate_mongo_secret_details(secret_string):
    #         try:
    #             connection_uri = MONGO_CONNECTION_STRING.format(
    #                 user_name=secret_string["username"],
    #                 password=secret_string["password"],
    #                 host_name=secret_string["host"]
    #             )
    #             return connection_uri

    #         except KeyError as e:
    #             logger.error(f"Missing key while preparing connection string: {str(e)}")
    #             return None

    #     logger.error("Mongo secret validation failed. Missing parameters.")
    #     return None

    # -------------------------------------------------------
    # GET DATABASE INSTANCE
    # -------------------------------------------------------
    def get_database_instance(self, connection_string, database_name):
        try:
            logger.info(f"Connecting to MongoDB database: {database_name}")
            client = MongoClient(connection_string)
            return client[database_name]

        except (pymongo.errors.ConnectionFailure, pymongo.errors.PyMongoError) as exception:
            logger.error(f"Unable to connect to MongoDB ({database_name})")
            logger.error(str(exception))
            return None

    # -------------------------------------------------------
    # INITIALIZE MONGO USING AWS SECRETS MANAGER
    # -------------------------------------------------------
    # def initialize_mongo_db_instances(self, organization_id=None):
    #     # secrets_manager = AWSSecretsManagerUtil()

    #     # # Build secret key name
    #     # mongo_secret_key_name = SECRETS_MANAGER_MONGO_KEY_NAME_FORMAT.format(
    #     #     organization_id=str(organization_id)
    #     # )

    #     # logger.info(f"Fetching MongoDB credentials for org: {organization_id}")

    #     # # Fetch the secret from AWS
    #     # response = secrets_manager.get_value(mongo_secret_key_name)

    #     # if not response or "SecretString" not in response:
    #     #     logger.error("Failed to fetch credentials from AWS Secrets Manager")
    #     #     return None

    #     # # Load credentials JSON
    #     # credentials = json.loads(response["SecretString"])

    #     # Prepare URI
    #     connection_string = MONGO_CONNECTION_STRING
    #     if not connection_string:
    #         return None

    #     # Get DB instance
    #     self.database_instance = self.get_database_instance(
    #         connection_string,
    #         MAPPING_DATABASE_NAME
    #     )

        # # SAFE CHECK (Cannot use if self.database_instance)
        # if self.database_instance is not None:
        #     logger.info("MongoDB initialized successfully")

        # return self.database_instance

    # -------------------------------------------------------
    # GET COLLECTION (Auto Init DB)
    # -------------------------------------------------------
    # def get_collection(self, collection_name="ReconciliationLog", organization_id=None):
    #     # Initialize DB if not already initialized
    #     if self.database_instance is None:
    #         logger.info("MongoDB not initialized — initializing now.")
    #         self.initialize_mongo_db_instances(organization_id)

    #     # Still None? -> Failure
    #     if self.database_instance is None:
    #         logger.error("Database instance is unavailable")
    #         return None

    #     try:
    #         collection = self.database_instance[collection_name]
    #         logger.info(f"Connected to collection: {collection_name}")
    #         return collection

    #     except Exception as e:
    #         logger.error(f"Error fetching collection {collection_name}: {str(e)}")
    #         return None
