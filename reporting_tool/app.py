from flask import Flask, render_template, request
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from configuration.constants import *


from helper.logic import LogProcessor
from utilities.MongoDBOperations import DataRetriever
from utilities.MongoDBUtils import DatabaseConnector

load_dotenv()

app = Flask(__name__)

# Initialize DB once
db_connector = DatabaseConnector()
collection = db_connector.database_instance[COLLECTION_NAME]


# ---------------------------------------------------------
# ✅ Separated Date Logic Into Dedicated Helper Function
# ---------------------------------------------------------
def get_date_range(request):
    """Handles all date logic for GET & POST."""

    # Default → last 7 days
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)

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

    return start_date, end_date


# ---------------------------------------------------------
# MAIN ROUTE — Clean & Production Level
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    # 1. Get dates from helper function
    start_date, end_date = get_date_range(request)

    # 2. Get logs from MongoDB
    retriever = DataRetriever(db_connector.database_instance)
    logs = retriever.retrieve_issue_inquiry_logs(COLLECTION_NAME,start_date, end_date)

    # 3. Process logs
    processor = LogProcessor(logs)
    result_dict = processor.run()

    # 4. Render page
    return render_template(
        "index.html",
        data=result_dict,
        start_date=start_date,
        end_date=end_date,
    )


if __name__ == "__main__":
    app.run(debug=False)
