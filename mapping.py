# jotform_calendar_tool/utils/mapping.py
def normalize_department(value: str) -> str:
    lookup = {
        "Lang": "Language Center",
        "B&P": "Business & Policy",
        "Film": "Film, Culture & Community",
        "Edu": "Education & Family",
        "Tech": "Information Technology",
        "Admin": "Administration",
        "Dev": "Development",
        "HR": "Human Resources",
        "PA": "Performing Arts",
        "Gallery": "Gallery",
        "C&C": "Film, Culture & Community",
        "Exec": "Office of the President",
        "SE": "Special Events",
        "Talks": "Film, Culture & Community",
        "Rentals": "Rentals",
    }
    clean = value.strip()
    return lookup.get(clean, clean)

def should_skip_department(dept: str) -> bool:
    return dept.strip().lower() in {"talks", "c&c", "se", "rentals", "holiday"}
