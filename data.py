# By Yasin ==> TG : @Rapcher
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("data.json")

START_T0 = datetime(2025, 9, 23)
END_T0 = datetime(2026, 7, 22)

TOTAL_U = 88
TOTAL_C = 88


def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            return {}

        data = json.loads(content)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError):
        print("WARNING: data.json is empty or invalid.")
        print("Starting with an empty database.")
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def random_t0():
    if random.random() < 0.85:
        start = datetime(2026, 5, 22)
        end = datetime(2026, 7, 22)
    else:
        start = START_T0
        end = END_T0

    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1

    import calendar

    day = min(
        date.day,
        calendar.monthrange(year, month)[1]
    )

    return date.replace(
        year=year,
        month=month,
        day=day
    )


def generate_codes():
    u = [f"u{i:02d}" for i in range(1, 100)]
    c = [f"c{i:02d}" for i in range(1, 100)]

    selected_u = random.sample(u, TOTAL_U)
    selected_c = random.sample(c, TOTAL_C)

    codes = selected_u + selected_c
    random.shuffle(codes)

    return codes


def create_schedule(data):
    codes = generate_codes()

    for code in codes:
        if code in data:
            continue

        t0 = random_t0()

        t1 = t0 + timedelta(
            days=random.randint(45, 50)
        )

        t2 = add_months(t0, 3)

        data[code] = {
            "group": code[0],
            "T0": {
                "date": t0.strftime("%Y-%m-%d"),
                "completed": False
            },
            "T1": {
                "date": t1.strftime("%Y-%m-%d"),
                "completed": False
            },
            "T2": {
                "date": t2.strftime("%Y-%m-%d"),
                "completed": False
            }
        }

    save_data(data)

    print(f"Created {len(codes)} participant schedules.")


def show_schedule(data):
    for code, participant in data.items():
        print(
            code,
            "|",
            participant["group"],
            "| T0:", participant["T0"]["date"],
            "| T1:", participant["T1"]["date"],
            "| T2:", participant["T2"]["date"]
        )


def main():
    data = load_data()

    if not data:
        create_schedule(data)
        data = load_data()

    show_schedule(data)


if __name__ == "__main__":
    main()