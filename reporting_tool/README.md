# Reporting Tool Service

A Flask-based web application for retrieving and analyzing issue inquiry logs from MongoDB. The application provides a user-friendly interface to view and filter logs based on date ranges.

## Features

- View issue inquiry logs from MongoDB
- Filter logs by date range (last 24 hours, last 7 days, or custom range)
- Display token usage statistics (input, output, and total tokens)
- Track interaction counts and retry information

## Prerequisites

- Python 3.10+
- MongoDB instance
- AWS Secrets Manager (for production secrets)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Reporting_Tool_Service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv_reporting_tool
   .\venv_reporting_tool\Scripts\activate  # On Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r reporting_tool/requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   MONGODB_URI=your_mongodb_connection_string
   DATABASE_NAME=your_database_name
   COLLECTION_NAME=your_collection_name
   ```

2. For production, ensure AWS credentials are configured for Secrets Manager access.

## Running the Application

1. Activate the virtual environment if not already activated:
   ```bash
   .\venv_reporting_tool\Scripts\activate  # On Windows
   ```

2. Run the Flask application:
   ```bash
   cd reporting_tool
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
reporting_tool/
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── configuration/        # Configuration files
│   ├── constants.py     # Application constants
│   └── Logger.py        # Logging configuration
├── helper/
│   └── logic.py         # Core business logic for log processing
├── static/              # Static files (CSS, JS, images)
│   └── index.css        # Custom styles
├── templates/           # HTML templates
│   └── index.html       # Main application view
└── utilities/           # Utility classes
    ├── MongoDBOperations.py  # MongoDB data retrieval
    └── MongoDBUtils.py       # MongoDB connection handling
```

## API Endpoints

- `GET /` - Main dashboard displaying logs and statistics
  - Supports filtering by date range via POST request

## Dependencies

- Flask - Web framework
- pymongo - MongoDB Python driver
- python-dotenv - Environment variable management
- pandas - Data manipulation (if needed for future enhancements)

## Logging

Logs are stored in `reporting_tool/logs/logs.txt` with the following format:
- INFO: General application information
- ERROR: Error messages and exceptions

