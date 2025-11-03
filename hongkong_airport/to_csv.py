import csv
import json
import os
import sys
from typing import Any, Iterable


try:
    from . import config  # type: ignore
except Exception:  # pragma: no cover
    import importlib
    config = importlib.import_module("config")


def _safe_join(values: Iterable[Any]) -> str:
    parts = []
    for v in values or []:
        if v is None:
            continue
        parts.append(str(v))
    return "|".join(parts)


def _derive_output_path(json_path: str) -> str:
    base, ext = os.path.splitext(json_path)
    return f"{base}.csv"


def to_csv(input_json_path: str | None = None, output_csv_path: str | None = None) -> int:
    src_path = input_json_path or getattr(config, "out", "./flights.json")
    if not src_path:
        print("Input JSON path not provided and config.out is empty", file=sys.stderr)
        return 1

    dst_path = output_csv_path or _derive_output_path(src_path)

    try:
        with open(src_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Input file not found: {src_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {src_path}: {e}", file=sys.stderr)
        return 3

    # Expecting a list of day-level dicts
    if not isinstance(data, list):
        print("Unexpected JSON format: expected a list at top-level", file=sys.stderr)
        return 4

    # CSV columns
    fieldnames = [
        "date",
        "arrival",
        "cargo",
        "time",
        "status",
        "statusCode",
        "origin",
        "baggage",
        "hall",
        "terminal",
        "stand",
        "flight_nos",
        "flight_airlines",
        "lastUpdatedTime",
    ]

    with open(dst_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for day in data:
            if not isinstance(day, dict):
                continue
            date_str = day.get("date", "")
            arrival_flag = day.get("arrival", "")
            cargo_flag = day.get("cargo", "")
            last_updated = day.get("lastUpdatedTime", "")

            flights = day.get("list", []) or []
            for item in flights:
                # Flatten fields
                time_str = item.get("time", "")
                status = item.get("status", "")
                status_code = item.get("statusCode", "")
                origin = _safe_join(item.get("origin", []))
                baggage = item.get("baggage", "")
                hall = item.get("hall", "")
                terminal = item.get("terminal", "")
                stand = item.get("stand", "")

                # Flight numbers and airlines are arrays of objects
                flight_list = item.get("flight", []) or []
                flight_nos = _safe_join(x.get("no") for x in flight_list if isinstance(x, dict))
                flight_airlines = _safe_join(x.get("airline") for x in flight_list if isinstance(x, dict))

                writer.writerow(
                    {
                        "date": date_str,
                        "arrival": arrival_flag,
                        "cargo": cargo_flag,
                        "time": time_str,
                        "status": status,
                        "statusCode": status_code,
                        "origin": origin,
                        "baggage": baggage,
                        "hall": hall,
                        "terminal": terminal,
                        "stand": stand,
                        "flight_nos": flight_nos,
                        "flight_airlines": flight_airlines,
                        "lastUpdatedTime": last_updated,
                    }
                )

    print(f"CSV written to {dst_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(to_csv())


