# jotform_calendar_tool/scripts/test_upload.py
import csv, requests, sys
from config import API_KEY, FORM_ID, BASE_URL, validate_config

# Validate config
validate_config()

# Map QIDs to Jotform fields
QIDS = {
    "Day": 3,
    "Date": 4,
    "Department": 5,
    "Event Name": 6,
    "Hold Times": 7,
    "Event Start Time": 8,
    "Event End Time": 9,
    "Location": 10,
    "Status": 11,
    "Check-in Time": 12,
    "AUD Doors": 13,
    "Run Time": 14,
    "Description / Notes": 15
}

# Match CSV keys to Jotform labels
FIELD_MAP = {
    "day": "Day",
    "date": "Date",
    "department": "Department",
    "event name": "Event Name",
    "hold times": "Hold Times",
    "event start time": "Event Start Time",
    "event end time": "Event End Time",
    "location": "Location",
    "status": "Status",
    "check-in time": "Check-in Time",
    "aud doors": "AUD Doors",
    "run time": "Run Time",
    "description / notes": "Description / Notes"
}

def post_test_row(row: dict) -> str:
    payload = {
        f"submission[{QIDS[label]}]": row.get(csv_key, "")
        for csv_key, label in FIELD_MAP.items()
        if label in QIDS
    }
    url = f"{BASE_URL}/form/{FORM_ID}/submissions"
    response = requests.post(url, params={"apiKey": API_KEY}, data=payload, timeout=15)
    data = response.json()
    if "submissionID" in data:
        return data["submissionID"]
    print(f"Failed: {data}")
    return ""

def main():
    file_path = "data/events_clean.csv"
    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            test_row = next(reader, None)
            if not test_row:
                sys.exit("No data found in CSV.")
    except FileNotFoundError:
        sys.exit(f"File not found: {file_path}")

    print("Testing upload of 1 record...")
    result = post_test_row(test_row)
    if result:
        print(f"Test upload succeeded: {result}")
    else:
        print("Test upload failed.")

if __name__ == "__main__":
    main()
