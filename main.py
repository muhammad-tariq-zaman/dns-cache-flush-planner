"""Plan a DNS cache flush from a CSV of cached records.

Usage: python3 main.py cache.csv --os linux --expiring-within 60
CSV columns: hostname,record_type,ttl_remaining_seconds
Entries already expired or expiring within the threshold are flushed now;
healthy entries are left alone. Prints the OS flush command to run.
"""
import argparse
import csv
import sys

FLUSH_COMMANDS = {
    "windows": "ipconfig /flushdns",
    "linux": "resolvectl flush-caches",
    "macos": "dscacheutil -flushcache; killall -HUP mDNSResponder",
}


def classify(ttl, threshold):
    if ttl <= 0:
        return "EXPIRED"
    if ttl <= threshold:
        return "EXPIRING"
    return "CACHED"


def plan(rows, threshold):
    result = []
    for row in rows:
        ttl = int(row["ttl_remaining_seconds"])
        result.append((row["hostname"], row["record_type"], ttl, classify(ttl, threshold)))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="CSV with hostname,record_type,ttl_remaining_seconds")
    parser.add_argument("--os", choices=sorted(FLUSH_COMMANDS), default="linux")
    parser.add_argument("--expiring-within", type=int, default=60)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        entries = plan(list(csv.DictReader(f)), args.expiring_within)
    flush_now = [e for e in entries if e[3] in ("EXPIRED", "EXPIRING")]
    for host, rtype, ttl, state in entries:
        print(f"{host} ({rtype}): {state} ({ttl}s remaining)")
    print(f"Flush now: {len(flush_now)}/{len(entries)} entries.")
    if flush_now:
        print(f"Run: {FLUSH_COMMANDS[args.os]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
