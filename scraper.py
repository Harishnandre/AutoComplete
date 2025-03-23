import requests
import time

# API Endpoint
API_URL = "http://35.200.185.69:8000/v3/autocomplete?query={}"

# Set to store discovered names
discovered_names = set()

# Counter for API requests
request_count = 0  

# Function to make requests with exponential backoff
def fetch_names(query, retries=3, delay=2):
    global request_count  # Track number of requests
    for attempt in range(retries):
        try:
            response = requests.get(API_URL.format(query))
            request_count += 1  # Increment request count

            # Rate limit handling
            if response.status_code == 429:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exceeded. Sleeping for {wait_time}s...")
                time.sleep(wait_time)
                continue

            # Extract JSON response
            if response.status_code == 200:
                return response.json().get("results", [])

        except requests.RequestException as e:
            print(f"Error fetching {query}: {e}")
            time.sleep(1)  # Short delay before retrying

    return []  # Return empty if all retries fail

# Function to recursively explore names
def extract_all_names():
    global request_count
    all_chars = list("abcdefghijklmnopqrstuvwxyz0123456789-+.")  # Start with a-z, 0-9 or special characters
    queue = all_chars[:]  # Initialize queue with base characters

    while queue:
        prefix = queue.pop(0)  # Get next prefix to explore
        names = fetch_names(prefix)

        for name in names:
            if name not in discovered_names:
                discovered_names.add(name)
                if len(name) < 10:  # Limit expansion to avoid excessive queries
                    queue.append(name)  

        print(f"Checked: {prefix} | Found: {len(names)} new names | Total: {len(discovered_names)} | Requests: {request_count}")
        time.sleep(0.5)  # Respect API limits

# Run the extraction process
extract_all_names()

# Save results to a file
with open("collected_names.txt", "w") as f:
    for name in sorted(discovered_names):
        f.write(name + "\n")

print(f"Extraction complete! {len(discovered_names)} names saved to collected_names.txt.")
print(f"Total API requests made: {request_count}")
