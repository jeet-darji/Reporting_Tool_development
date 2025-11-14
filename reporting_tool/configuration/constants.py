# ==============================
# PRODUCTION CONSTANTS
# ==============================

# Tenant ID used in LogProcessor
DEFAULT_TENANT_ID = 2111

# Event contextual keys (in case structure changes later)
EVENT_CONTEXT_KEY = "eventObject"
EVENT_CONTEXT_INFO_KEY = "eventContextualInformation"

# Event attribute keys
INTERACTION_COUNT_KEY = "interactionCount"
TOKEN_COUNT_KEY = "totalTokenCount"
TOKEN_INPUT_KEY = "inputTokens"
TOKEN_OUTPUT_KEY = "outputTokens"
TOKEN_TOTAL_KEY = "totalTokenCounts"
PIPELINE = "pipeline"
# Retry keys
BATCH_RETRY_DETAILS_KEY = "batchRetryDetails"
RETRY_DETAILS_KEY = "retryDetails"

# Default retry result
DEFAULT_RETRY_INFO = {"retry_count": 0}
MONGO_CONNECTION_STRING = "mongodb+srv://intEUCluster:EpmB1q2zBXu2Lv14@int-eu-cluster.fekpn.mongodb.net/"
MAPPING_DATABASE_NAME = "DoMaster"
COLLECTION_NAME = "ReconciliationLog"
SECRETS_MANAGER_MONGO_KEY_NAME_FORMAT = """do-ndb-mng-cdm-org{organization_id}-secret"""
MONGO_CONNECTION_STRING_TENANT_WISE = """mongodb+srv://{user_name}:{password}@{host_name}/"""