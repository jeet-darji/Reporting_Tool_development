from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from flask import Flask, render_template, request
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from configuration.constants import *
from utilities import MongoURIManager

from helper.logic import LogProcessor
from utilities.MongoDBOperations import DataRetriever
from utilities.MongoDBUtils import DatabaseConnector

load_dotenv()

app = Flask(__name__)

# Initialize DB once
db_connector = DatabaseConnector()
# collection = db_connector.database_instance[COLLECTION_NAME]


# ---------------------------------------------------------
# ✅ Separated Date Logic Into Dedicated Helper Function
# ---------------------------------------------------------
def get_date_range_and_tenant_ids(request):
    """Handles all date logic for GET & POST."""

    # Default → last 7 days
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    tenant_ids = [2128]
    if request.method == "POST":
        quick_filter = request.form.get("quick_filter", "")

        # Quick Filter Options
        if quick_filter == "24h":
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(hours=24)

        elif quick_filter == "7d":
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=7)

        else:
            # Manual date range input
            start_date = datetime.strptime(
                request.form["start_date"], "%Y-%m-%dT%H:%M"
            ).replace(tzinfo=timezone.utc)

            end_date = datetime.strptime(
                request.form["end_date"], "%Y-%m-%dT%H:%M"
            ).replace(tzinfo=timezone.utc)
            
        tenant_input = request.form["tenant_ids"]
        if not tenant_input :
            tenant_ids = [2128]
        else : 
            tenant_ids = [tid.strip() for tid in tenant_input.replace("\n", ",").split(",") if tid.strip()]

    return start_date, end_date,tenant_ids


def fetch_and_process_all_tenants(tenant_ids, start_date, end_date, max_workers=8):
    """
    Fetch logs and process data for multiple tenants concurrently.
    """
    final_dict = {}

    def process_single_tenant(tenant_id):
        """
        Handles data retrieval + processing for a single tenant.
        """
        try:
            uri_manager = MongoURIManager(tenant_id)
            db_connector = DatabaseConnector(uri_manager.get_mongo_uri())
            retriever = DataRetriever(db_connector.database_instance)
            logs = retriever.retrieve_issue_inquiry_logs(COLLECTION_NAME, start_date, end_date)
            processor = LogProcessor(logs)
            result_dict = processor.run()
            logging.info(f"✅ Successfully processed tenant {tenant_id}")
            return tenant_id, result_dict
        except Exception as e:
            logging.error(f"❌ Error processing tenant {tenant_id}: {e}")
            return tenant_id, None

    logging.info(f"Starting multi-threaded data fetch for {len(tenant_ids)} tenants...")

    with ThreadPoolExecutor(max_workers=min(len(tenant_ids), max_workers)) as executor:
        futures = {executor.submit(process_single_tenant, tid): tid for tid in tenant_ids}

        for future in as_completed(futures):
            tenant_id = futures[future]
            try:
                tid, result = future.result()
                final_dict[tid] = result
            except Exception as e:
                logging.error(f"Error retrieving result for tenant {tenant_id}: {e}")
                final_dict[tenant_id] = None

    logging.info("✅ All tenant data processed successfully.")
    return final_dict


# ---------------------------------------------------------
# MAIN ROUTE — Clean & Production Level
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    # 1. Get dates from helper function
    start_date, end_date,tenant_ids = get_date_range_and_tenant_ids(request)
    # this is the final line for change 
    # final_dict = fetch_and_process_all_tenants(tenant_ids,start_date,end_date)
    
    final_dict = {}

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(lambda tid: (tid,LogProcessor(DataRetriever(DatabaseConnector().database_instance).retrieve_issue_inquiry_logs(COLLECTION_NAME, start_date, end_date)).run()), i): i for i in tenant_ids}

        for future in as_completed(futures):
            tenant_id, result_dict = future.result()
            final_dict[tenant_id] = result_dict
    
    # 4. Render page
    return render_template(
        "index.html",
        final_data=final_dict,
        start_date=start_date,
        end_date=end_date,
    )

if __name__ == "__main__":
    app.run(debug=False)
