import requests
import time

# Configuration
url = "http://localhost:8000/api/v1/books/1"
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
total_requests = 20  # Change based on your rate limit expectations
delay_between_requests = 0.5  # seconds, tweak to avoid instant bursts

print(f"Testing rate limit on {url} with {total_requests} requests:")

for i in range(total_requests):
    response = requests.get(url, headers=headers)
    status = response.status_code
    print(f"[{i+1}] Status: {status}")

    # Optional: Check for headers related to rate limits
    if 'Retry-After' in response.headers:
        print(f"    > Retry-After: {response.headers['Retry-After']}")

    if 'X-RateLimit-Remaining' in response.headers:
        print(f"    > Remaining: {response.headers['X-RateLimit-Remaining']}")

    if status == 429:
        print("    > Rate limit hit!")
        break

    time.sleep(delay_between_requests)
