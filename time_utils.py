#time_utils.py
def normalize_time(t: str) -> str:
    import re
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
    import re
    if not isinstance(text, str):
        return "", ""
    if "all day" in text.lower():
        return "00:00", "23:59"
    parts = re.split(r"\s*[-–—]\s*", text, maxsplit=1)
    if len(parts) == 2:
        from .time_utils import normalize_time
        return normalize_time(parts[0]), normalize_time(parts[1])
    return "", ""

