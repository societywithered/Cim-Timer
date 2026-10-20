#!/usr/bin/env python3
import re
import sys
import time


def parse_duration(value):
    """Parse a duration such as 30s, 5m, or 1h."""
    match = re.fullmatch(r"(\d+)([smh]?)", value.lower())

    if not match:
        raise ValueError("Use a duration like 30s, 5m, or 1h.")

    amount = int(match.group(1))
    unit = match.group(2) or "s"
    multipliers = {"s": 1, "m": 60, "h": 3600}
    seconds = amount * multipliers[unit]

    if seconds <= 0:
        raise ValueError("Duration must be greater than zero.")

    return seconds


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: cim-timer DURATION")
        print("Examples: cim-timer 30s | cim-timer 5m | cim-timer 1h")
        return 0 if len(sys.argv) == 2 else 2

    try:
        remaining = parse_duration(sys.argv[1])
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    try:
        while remaining > 0:
            print(f"\rTime remaining: {format_time(remaining)}", end="", flush=True)
            time.sleep(1)
            remaining -= 1

        print("\rTime remaining: 00:00")
        print("\aTimer finished!")
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())