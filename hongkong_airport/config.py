from datetime import datetime

# Configuration for Hong Kong Airport flight crawler

# Time range in days to query (API span)
span = 1

# Date in YYYY-MM-DD. Automatically set to today's date from system time
date = datetime.now().strftime("%Y-%m-%d")

# How many days before the base date to include (integer >= 0)
previous_days = 91

# How many days after the base date to include (integer >= 0)
future_days = 14

# Language code: "en" (English), "tc" (Traditional Chinese), "sc" (Simplified Chinese)
lang = "en"

# Include cargo flights
cargo = False

# True for arrivals, False for departures
arrival = True

# Optional path to save raw JSON response (e.g., "flights.json").
# If None, will print to stdout
out = "./flights.json"


