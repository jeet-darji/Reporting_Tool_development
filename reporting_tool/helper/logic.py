import pandas as pd
from configuration.constants import (
    DEFAULT_TENANT_ID,
    EVENT_CONTEXT_KEY,
    EVENT_CONTEXT_INFO_KEY,
    INTERACTION_COUNT_KEY,
    TOKEN_COUNT_KEY,
    TOKEN_INPUT_KEY,
    TOKEN_OUTPUT_KEY,
    TOKEN_TOTAL_KEY,
    BATCH_RETRY_DETAILS_KEY,
    RETRY_DETAILS_KEY,
    DEFAULT_RETRY_INFO,
    PIPELINE
)

class LogProcessor:
    def __init__(self, logs, logger=None):
        self.logs = logs
        self.logger = logger
        self.tenants = []
        self.pipeline = []
        self.input_tokens = []
        self.output_tokens = []
        self.total_tokens = []
        self.interaction_counts = []
        self.retries_count = []

    def log(self, message):
        if self.logger:
            self.logger.info(message)
    # needs to implement logic here for multiple tenants
    def process_log(self, log):
        try:
            # Add tenant ID from constants
            self.tenants.append(DEFAULT_TENANT_ID)
            # Retrieve event context
            event_context = log[EVENT_CONTEXT_KEY][EVENT_CONTEXT_INFO_KEY]
            
            if isinstance(event_context[PIPELINE], list):
                self.pipeline.append(event_context[PIPELINE][0])
            else :
                self.pipeline.append(event_context[PIPELINE])
            # Interaction Count 
            self.interaction_counts.append(event_context[INTERACTION_COUNT_KEY])

            # Tokens
            tokens = event_context[TOKEN_COUNT_KEY]
            self.input_tokens.append(tokens[TOKEN_INPUT_KEY])
            self.output_tokens.append(tokens[TOKEN_OUTPUT_KEY])
            self.total_tokens.append(tokens[TOKEN_TOTAL_KEY])

            # Retry processing
            batch_retry_details = event_context[BATCH_RETRY_DETAILS_KEY]
            # retry_dict = {}
            retry_count = 0
            for obj in batch_retry_details:
                retry_info = obj.get(RETRY_DETAILS_KEY)

                if isinstance(retry_info, dict):
                    retry_count += len(retry_info)
            self.retries_count.append(retry_count)
            # Append retry result
            # self.retries_count.append(retry_dict if retry_dict else DEFAULT_RETRY_INFO)

        except Exception as e:
            if self.logger:
                self.logger.error(f"Skipping malformed log: {e}")

    def run(self):
        for log in self.logs:
            self.process_log(log)
        
        df = pd.DataFrame({
            "tenant": self.tenants,
            "pipeline" : self.pipeline,
            "interaction_processed": self.interaction_counts,
            "inputTokens": self.input_tokens,
            "outputTokens": self.output_tokens,
            "totalTokens": self.total_tokens,
            "retries_count": self.retries_count,
        })
        
        grouped_df = (df.groupby("pipeline", as_index=False).agg({
                                                        "interaction_processed": "sum",
                                                        "inputTokens": "sum",
                                                        "outputTokens": "sum",
                                                        "totalTokens": "sum",
                                                        "retries_count": "sum"}))
        
        resultant_dict = grouped_df.to_dict(orient='list')
        
        # Final output
        return resultant_dict
