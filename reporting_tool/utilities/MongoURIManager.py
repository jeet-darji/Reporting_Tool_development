import json
import logging
from utilities.aws_secret_trial import AWSSecretManager


class MongoURIManager:
    """
    Handles AWS secret retrieval and MongoDB URI generation.
    """

    def __init__(self, tenant_id: str):
        """
        Initialize with tenant ID.
        """
        self.tenant_id = tenant_id
        self.secret_data = None
        self.mongo_uri = None

    def fetch_secrets(self) -> bool:
        """
        Fetch secrets from AWS Secrets Manager.
        Returns True if successful, False otherwise.
        """
        try:
            logging.info(f"Fetching AWS secrets for tenant ID: {self.tenant_id}")
            secret_manager = AWSSecretManager()
            secret_response = secret_manager.get_secret(self.tenant_id)

            if not secret_response or "SecretString" not in secret_response:
                logging.error(f"No secrets found or invalid response for tenant {self.tenant_id}")
                return False

            self.secret_data = json.loads(secret_response["SecretString"])
            logging.info(f"✅ Successfully fetched and parsed secrets for tenant {self.tenant_id}")
            return True

        except json.JSONDecodeError:
            logging.exception(f"Failed to decode secret JSON for tenant {self.tenant_id}")
            return False
        except Exception as e:
            logging.exception(f"Unexpected error while fetching secret for tenant {self.tenant_id}: {e}")
            return False

    def build_mongo_uri(self) -> str:
        """
        Build MongoDB connection URI using fetched secret data.
        """
        if not self.secret_data:
            logging.error("Cannot build Mongo URI: secrets not loaded.")
            raise ValueError("Secrets not loaded. Call fetch_secrets() first.")

        try:
            username = self.secret_data.get("username")
            password = self.secret_data.get("password")
            host = self.secret_data.get("host")

            if not all([username, password, host]):
                raise ValueError("Incomplete credentials in secret data.")

            self.mongo_uri = f"mongodb+srv://{username}:{password}@{host}"
            logging.info(f"✅ Mongo URI built successfully for tenant {self.tenant_id}")
            return self.mongo_uri

        except Exception as e:
            logging.exception(f"Failed to build Mongo URI for tenant {self.tenant_id}: {e}")
            raise

    def get_mongo_uri(self) -> str:
        """
        High-level function to fetch secrets and return Mongo URI.
        """
        if self.fetch_secrets():
            return self.build_mongo_uri()
        else:
            logging.error(f"❌ Failed to fetch Mongo URI for tenant {self.tenant_id}")
            return None