# jotform_calendar_tool/scripts/clean_csv.py
import pandas as pd
import re
import argparse
from dateutil import parser as dparser
from pathlib import Path

def parse_date(txt: str) -> str:
    try:
        dt = dparser.parse(txt, dayfirst=True, default=pd.Timestamp('2025-01-01'))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""

def norm_time(t: str) -> str:
    match = re.search(r"(\d{1,2}):(\d{2})\s*([ap]m)?", str(t), re.I)
    if not match:
        return ""
    h, m, tag = int(match[1]), int(match[2]), (match[3] or '').lower()
    if tag == "pm" and h != 12:
        h += 12
    elif tag == "am" and h == 12:
        h = 0
    return f"{h:02d}:{m:02d}"

def split_range(text: str) -> tuple[str, str]:
    if not isinstance(text, str):
        return "", ""
    if "all day" in text.lower():
        return "00:00", "23:59"
    parts = re.split(r"\s*[-–—]\s*", text, maxsplit=1)
    if len(parts) == 2:
        return norm_time(parts[0]), norm_time(parts[1])
    return "", ""

def clean_csv(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    df.columns = (df.columns
                    .str.replace('\ufeff', '', regex=False)
                    .str.replace(r'[-_]', ' ', regex=True)
                    .str.strip()
                    .str.casefold())

    aliases = {
        "day": ["day"],
        "date": ["date"],
        "department": ["dept", "department"],
        "event name": ["event name"],
        "hold times": ["hold times", "hold time"],
        "eventtimesraw": ["event times"],
        "event start time": ["event start time", "start time"],
        "event end time": ["event end time", "end time"],
        "location": ["location"],
        "status": ["status"],
        "check-in time": ["check-in time", "check in time"],
        "aud doors": ["aud doors"],
        "run time": ["run time"],
        "description / notes": ["description / notes", "notes"]
    }

    canon_map = {alias: canon for canon, alias_list in aliases.items() for alias in alias_list}
    df.rename(columns=canon_map, inplace=True)

    required = ["day", "date", "department", "event name", "location", "status"]
    missing = [r for r in required if r not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

    df["date"] = df["date"].apply(parse_date)
    df = df[df["date"] != ""]

    if "eventtimesraw" in df.columns:
        times = df["eventtimesraw"].apply(split_range).apply(pd.Series)
        df["event start time"], df["event end time"] = times[0], times[1]

    for col in ["check-in time", "aud doors"]:
        if col in df.columns:
            df[col] = df[col].apply(norm_time)

    if "run time" in df.columns:
        df["run time"] = df["run time"].str.extract(r"(\d+)")[0].fillna("")

    final_cols = required + [c for c in ["event start time", "event end time", "check-in time", "aud doors"] if c in df.columns] + ["hold times", "run time", "description / notes"]
    df[final_cols].to_csv(output_path, index=False)
    print(f"✅ Cleaned CSV written to {output_path} ({len(df)} rows)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input raw CSV path")
    parser.add_argument("-o", "--output", default="data/events_clean.csv", help="Cleaned output CSV path")
    args = parser.parse_args()
    clean_csv(args.input, args.output)

if __name__ == "__main__":
    main()
