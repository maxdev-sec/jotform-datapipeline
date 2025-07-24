# jotform_calendar_tool/scripts/upload.py
import csv, time, requests, sys
from config import API_KEY, FORM_ID, BASE_URL, validate_config

# Make sure env vars are loaded
validate_config()

# QID mapping based on Jotform fields
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

# Map CSV keys to Jotform field labels
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

def post_row(row: dict) -> str:
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
    print(f"✘ Failed submission: {data}")
    return ""

def main():
    file_path = "data/events_clean.csv"
    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        sys.exit(f"File not found: {file_path}")
      
    print(f" Uploading {len(rows)} rows from {file_path}...")
    uploaded = 0
    for i, row in enumerate(rows, 1):
        sid = post_row(row)
        if sid:
            uploaded += 1
            print(f"  {i:03d} ✔ Sent {sid}")
        else:
            print(f"  {i:03d} ✘ Failed row: {row.get('event name', 'unknown')}")
        time.sleep(1.1)

    print(f"\n Upload complete. {uploaded}/{len(rows)} rows uploaded.")

if __name__ == "__main__":
    main()
