import json
import sys
from datetime import datetime, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


API_URL = (
    "https://www.hongkongairport.com/flightinfo-rest/rest/flights"
)

try:
    from . import config  # type: ignore
except Exception:  # pragma: no cover
    import importlib
    config = importlib.import_module("config")


def build_headers() -> dict:
    return {
        "referer": "https://www.hongkongairport.com/en/flights/arrivals/passenger.page",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "user-agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 "
            "Mobile Safari/537.36 Edg/141.0.0.0"
        ),
        "accept": "application/json, text/plain, */*",
    }


def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("date must be in YYYY-MM-DD format")


def fetch_flights(
    span: int,
    date_str: str,
    lang: str,
    include_cargo: bool,
    arrival: bool,
    timeout: float = 15.0,
) -> dict:
    params = {
        "span": span,
        "date": date_str,
        "lang": lang,
        "cargo": str(include_cargo).lower(),
        "arrival": str(arrival).lower(),
    }

    session = create_session()
    resp = session.get(
        API_URL,
        params=params,
        headers=build_headers(),
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    cfg_span = int(getattr(config, "span", 1))
    cfg_date = getattr(config, "date", None)
    if not cfg_date:
        cfg_date = datetime.now().strftime("%Y-%m-%d")
    cfg_lang = getattr(config, "lang", "en")
    cfg_cargo = bool(getattr(config, "cargo", False))
    cfg_arrival = bool(getattr(config, "arrival", True))
    cfg_out = getattr(config, "out", None)
    cfg_prev = int(getattr(config, "previous_days", 0))
    cfg_future = int(getattr(config, "future_days", 0))

    # validate
    try:
        validate_date(cfg_date)
    except Exception as e:
        print(f"Invalid date in config: {e}", file=sys.stderr)
        return 1

    # Build date range [D - previous_days, D + future_days]
    base_dt = datetime.strptime(cfg_date, "%Y-%m-%d")
    start_dt = base_dt - timedelta(days=cfg_prev)
    end_dt = base_dt + timedelta(days=cfg_future)

    # Aggregate results by date, merge lists if duplicated by span
    aggregated_by_date = {}

    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y-%m-%d")
        try:
            resp_data = fetch_flights(
                span=cfg_span,
                date_str=date_str,
                lang=cfg_lang,
                include_cargo=cfg_cargo,
                arrival=cfg_arrival,
            )
        except requests.HTTPError as http_err:
            print(f"HTTP error for {date_str}: {http_err}", file=sys.stderr)
            if http_err.response is not None:
                print(
                    f"Response {http_err.response.status_code}: {http_err.response.text[:500]}",
                    file=sys.stderr,
                )
            return 2
        except requests.RequestException as req_err:
            print(f"Request error for {date_str}: {req_err}", file=sys.stderr)
            return 3

        # resp_data is expected to be a list of day dictionaries
        if isinstance(resp_data, list):
            for day_obj in resp_data:
                d = day_obj.get("date")
                if not d:
                    continue
                if d not in aggregated_by_date:
                    aggregated_by_date[d] = {
                        "date": d,
                        "arrival": day_obj.get("arrival"),
                        "cargo": day_obj.get("cargo"),
                        "list": list(day_obj.get("list", [])),
                        "lastUpdatedTime": day_obj.get("lastUpdatedTime"),
                    }
                else:
                    # Merge flight lists
                    aggregated_by_date[d]["list"].extend(day_obj.get("list", []))
        else:
            # Fallback: store raw under the exact date
            if date_str not in aggregated_by_date:
                aggregated_by_date[date_str] = resp_data

        current_dt += timedelta(days=1)

    # Convert to list sorted by date
    data = [aggregated_by_date[k] for k in sorted(aggregated_by_date.keys())]

    if cfg_out:
        with open(cfg_out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(str(data))} bytes to {cfg_out}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

    # Simple summary to stdout
    try:
        summaries = []
        for day in data:
            date_str = day.get("date", "")
            flights = day.get("list", [])
            summaries.append(f"{date_str}: {len(flights)} records")
        if summaries:
            print("\nSummary:")
            for line in summaries:
                print(f"- {line}")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


