from datetime import datetime, timedelta
import pymongo
from configuration.Logger import Logger
from configuration.constants import *

logger = Logger().get_logger(__name__)


class DataRetriever:
    def __init__(self,db_instance):
        """
        # mongo_db_connection → the DB instance returned from DatabaseConnector.initialize_mongo_db_instances()
        """
        self.db = db_instance

    def retrieve_issue_inquiry_logs(self, collection_name, start_date, end_date):
        """
        Retrieve ISSUE_INQUIRY_GENERATION logs in a given date range.
        """
        try:
            collection = self.db[collection_name]

            query = {
                "eventObject.eventName": "ISSUE_INQUIRY_GENERATION",
                "doCreatedDate": {"$gte": start_date, "$lte": end_date}
            }

            logger.info(
                f"Retrieving ISSUE_INQUIRY_GENERATION logs from {collection_name} "
                f"between {start_date} and {end_date}"
            )

            logs = list(collection.find(query))

            logger.info(f"Retrieved {len(logs)} logs successfully")
            return logs

        except (pymongo.errors.OperationFailure,
                pymongo.errors.PyMongoError,
                Exception) as exception:
            logger.error(f"Failed to retrieve logs from {collection_name}")
            # logger.error(f"Query: {query}")
            logger.error(str(exception))

        return []
