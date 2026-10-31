# dns-cache-flush-planner

Decide which cached DNS records actually need flushing (expired or expiring soon) and print the right flush command for Windows, Linux or macOS, instead of flushing blindly.

## How to run

```sh
python3 main.py cache.csv --os linux --expiring-within 60
```

## Example output

```
web.example.com (A): EXPIRED (0s remaining)
mail.example.com (MX): CACHED (3600s remaining)
Flush now: 1/2 entries.
Run: resolvectl flush-caches
```

Standard library only. Run the tests with `python3 -m unittest discover`.
