# Configuration for Hong Kong Airport flight crawler

# Time range in days to query (API span)
span = 1

# Date in YYYY-MM-DD. Example: "2025-11-03"
# Leave as None to use today's date
date = "2025-11-03"

# Language code: "en" (English), "tc" (Traditional Chinese), "sc" (Simplified Chinese)
lang = "en"

# Include cargo flights
cargo = False

# True for arrivals, False for departures
arrival = True

# Optional path to save raw JSON response (e.g., "flights.json").
# If None, will print to stdout
out = "./flights.json"


