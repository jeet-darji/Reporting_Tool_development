import json
from utilities.aws_secret_trial import get_secret

tenant_id = input("Enter tenant ID  : ")
secrets = get_secret(tenant_id)
if secrets :
    response = secrets["SecretString"]
else :
    response = None
    print("Failed to fetch")
response = json.loads(response)
print(response)

mongo_URI = f"mongodb+srv://{response['username']}:{response['password']}@{response['host']}"
print(mongo_URI)
# pass this mongo URI to app.py and then retrieve data.py 