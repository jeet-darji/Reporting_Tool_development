import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

class AWSSecretManager:
    """
    AWS Secret Manager utility class.
    Fetches secrets from AWS Secrets Manager using a given profile and region.
    """

    def __init__(self, profile_name: str = "dataorb-main", region_name: str = "eu-central-1"):
        """
        Initialize AWS session and Secrets Manager client.
        """
        self.profile_name = profile_name
        self.region_name = region_name
        self.client = self._create_client()

    def _create_client(self):
        """
        Create and return a boto3 client for AWS Secrets Manager.
        """
        try:
            session = boto3.Session(profile_name=self.profile_name)
            client = session.client(service_name="secretsmanager", region_name=self.region_name)
            logging.info(f"AWS SecretsManager client created for profile: {self.profile_name}")
            return client
        except ProfileNotFound:
            logging.error(f"AWS profile '{self.profile_name}' not found. Check your AWS credentials.")
            raise
        except NoCredentialsError:
            logging.error("AWS credentials not found or invalid. Please configure them properly.")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while creating AWS client: {e}")
            raise

    def get_secret(self, org_id: str):
        """
        Retrieve a secret from AWS Secrets Manager by organization ID.
        """
        secret_name = f"do-uat-ndb-mng-cdm-org{org_id}-secret"
        try:
            logging.info(f"Fetching secret for org ID: {org_id} from region: {self.region_name}")
            response = self.client.get_secret_value(SecretId=secret_name)
            logging.info(f"Successfully fetched secret: {secret_name}")
            return response
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                logging.error(f"Secret not found: {secret_name}")
            elif e.response["Error"]["Code"] == "AccessDeniedException":
                logging.error(f"Access denied for secret: {secret_name}")
            else:
                logging.error(f"ClientError while fetching secret: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while fetching secret: {e}")
            return None