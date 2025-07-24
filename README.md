# README.md

## Jotform Calendar Import Tool

This tool imports structured calendar data from Excel/CSV into a Jotform table via API. It cleans, normalizes, and posts entries reliably.

## Directory Structure

```
jotform_calendar_tool/
├── .env                     # Store your Jotform API key & form ID
├── config.py                # Environment + base config
├── data/                    # Input/output files
│   ├── events.xlsx          # Original Excel file
│   └── events_clean.csv     # Output from cleaner
├── scripts/                 # CLI tools
│   ├── fix_quotes.py        # Fix malformed CSV quotes
│   ├── clean_csv.py         # Normalize and validate CSV
│   ├── upload.py            # Upload cleaned CSV rows
├── utils/                   # Shared logic
│   ├── time_utils.py        # parse/split/normalize time
│   └── mapping.py           # department lookups
└── README.md
```

## Setup

1. **Install dependencies**

```bash
pip install pandas python-dotenv requests
```

2. **Create `.env`**

```
JOTFORM_API_KEY=your_api_key_here
JOTFORM_FORM_ID=your_form_id_here
```

## How to Use

### 1. (Optional) Fix bad quotes

```bash
python scripts/fix_quotes.py -i data/raw.csv -o data/fixed.csv
```

### 2. Clean CSV for Jotform

```bash
python scripts/clean_csv.py -i data/fixed.csv -o data/events_clean.csv
```

### 3. Upload rowsbash

python scripts/upload.py

## Field Mapping Notes

- Input CSV headers like `event start time` are normalized.
- Time strings like `2:00pm - 5:00pm` are split into proper 24-hr fields.
- Departments are normalized (`Lang` → `Language Center`) and filtered if excluded.

## Result

Your Jotform table gets auto-populated with clean event data.

> Edit QIDs or mappings in `upload.py` or `utils/mapping.py` as your form changes.

## Built With Simplicity

- 100% CLI & Python
- Clear logs + validation
- Easy to plug into cron jobs or larger workflows
