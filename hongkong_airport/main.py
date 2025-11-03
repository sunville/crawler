import json
import sys
from datetime import datetime

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

    # validate
    try:
        validate_date(cfg_date)
    except Exception as e:
        print(f"Invalid date in config: {e}", file=sys.stderr)
        return 1

    try:
        data = fetch_flights(
            span=cfg_span,
            date_str=cfg_date,
            lang=cfg_lang,
            include_cargo=cfg_cargo,
            arrival=cfg_arrival,
        )
    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err}", file=sys.stderr)
        if http_err.response is not None:
            print(
                f"Response {http_err.response.status_code}: {http_err.response.text[:500]}",
                file=sys.stderr,
            )
        return 2
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}", file=sys.stderr)
        return 3

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


