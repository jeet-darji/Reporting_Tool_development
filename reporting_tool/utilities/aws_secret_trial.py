import boto3
from botocore.exceptions import ClientError

def get_secret(id):
    try :
        secret_name = f"do-uat-ndb-mng-cdm-org{id}-secret"
        region_name = "eu-central-1"

        # Use the SSO profile
        session = boto3.Session(profile_name="dataorb-main")

        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise e

        return response
    except Exception as e:
        print("Error while fetching secret : ", str(e)) 
        return None

# get_secret()
