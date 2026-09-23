# By Yasin ==> TG : @Rapcher
import json
import time
from datetime import datetime
from pathlib import Path

from form1 import run as run_form1
from form2 import run as run_form2
from form3 import run as run_form3

DATA_FILE = Path("data.json")


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
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()


def today():
    return datetime.now().date()


def run_timeline(code, timeline):
    print()
    print("=" * 50)
    print(f"Participant: {code}")
    print(f"Timeline: {timeline}")
    print("=" * 50)

    print("Form 1 started...")

    if not run_form1(code):
        print("Form 1 FAILED")
        return False

    print("Form 1 completed.")

    time.sleep(1)

    print("Form 2 started...")

    if not run_form2(code):
        print("Form 2 FAILED")
        return False

    print("Form 2 completed.")

    time.sleep(1)

    print("Form 3 started...")

    if not run_form3(code):
        print("Form 3 FAILED")
        return False

    print("Form 3 completed.")

    print()
    print(f"{code} | {timeline} | ALL FORMS COMPLETED")

    return True


def find_due_timelines(data):
    current = today()
    due = []

    for code, participant in data.items():
        for timeline in ["T0", "T1", "T2"]:
            item = participant.get(timeline)

            if not item:
                continue

            if item.get("completed") is True:
                continue

            try:
                scheduled = datetime.strptime(
                    item["date"],
                    "%Y-%m-%d"
                ).date()
            except:
                continue

            if scheduled <= current:
                due.append((scheduled, code, timeline))

    due.sort(key=lambda x: x[0])

    return due


def main():
    data = load_data()

    if not data:
        print("data.json is empty.")
        return

    due = find_due_timelines(data)

    if not due:
        print("No timelines are due today.")
        return

    print()
    print(f"{len(due)} timeline(s) ready.")
    print()

    for scheduled, code, timeline in due:
        print(
            f"{code} | {timeline} | "
            f"scheduled: {scheduled}"
        )

    for scheduled, code, timeline in due:

        print()
        print(
            f"Running {code} | {timeline} "
            f"| scheduled {scheduled}"
        )

        success = run_timeline(code, timeline)

        if success:
            data[code][timeline]["completed"] = True
            data[code][timeline]["completed_at"] = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            save_data(data)

            print(
                f"{code} | {timeline} | "
                f"saved as completed"
            )

        else:
            print(
                f"{code} | {timeline} | "
                f"FAILED - will retry later"
            )

        time.sleep(2)


if __name__ == "__main__":
    main()