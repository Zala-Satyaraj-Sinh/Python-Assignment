import json
import sys
from collections import defaultdict


def read_records(filename):
    """Generator: reads one JSON record at a time."""
    with open(filename, "r") as file:
        for line in file:
            try:
                record = json.loads(line)
                yield record
            except json.JSONDecodeError:
                # Completely invalid JSON line
                yield None


def etl_pipeline(filename):
    # Statistics stored only for each device
    stats = defaultdict(lambda: {
        "count": 0,
        "min": None,
        "max": None,
        "sum": 0.0,
        "corrupted": 0
    })

    for record in read_records(filename):

        # Invalid JSON
        if record is None:
            continue

        device_id = record.get("device_id")
        temperature = record.get("temperature_c")
        humidity = record.get("humidity")

        # Check required fields
        if device_id is None or temperature is None or humidity is None:
            if device_id is not None:
                stats[device_id]["corrupted"] += 1
            continue

        # Check numeric values
        try:
            temperature = float(temperature)
            humidity = float(humidity)
        except (ValueError, TypeError):
            stats[device_id]["corrupted"] += 1
            continue

        # Transform: Celsius → Fahrenheit
        temperature_f = (temperature * 9 / 5) + 32

        # Update statistics using original Celsius temperature
        s = stats[device_id]

        s["count"] += 1
        s["sum"] += temperature

        if s["min"] is None or temperature < s["min"]:
            s["min"] = temperature

        if s["max"] is None or temperature > s["max"]:
            s["max"] = temperature

    # Produce summary
    for device_id in sorted(stats):
        s = stats[device_id]

        if s["count"] > 0:
            average = s["sum"] / s["count"]
            print(
                f"{device_id} "
                f"count={s['count']} "
                f"min={s['min']:g} "
                f"max={s['max']:g} "
                f"avg={average:.2f} "
                f"corrupted={s['corrupted']}"
            )
        else:
            print(
                f"{device_id} count=0 "
                f"min=N/A max=N/A avg=N/A "
                f"corrupted={s['corrupted']}"
            )


if __name__ == "__main__":
    filename = input("Enter JSONL file path: ").strip()
    etl_pipeline(filename)