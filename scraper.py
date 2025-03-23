import requests
import time
from itertools import product
import string

# API configuration
base_url = "http://35.200.185.69:8000/v3/autocomplete"
unique_names = set()
lowercase_letters = string.ascii_lowercase
char_list = list(lowercase_letters)  + [str(x) for x in range(10)] + ['+', '-', ' ', '.']

# Global counter
request_count = 0

# Function to query API with retry mechanism for 429 errors
def query_api(query):
    global request_count  
    max_retries = 5  # Maximum retries for 429 errors
    delay = 2  # Initial delay in seconds

    for attempt in range(max_retries):
        try:
            print(f"Querying API with: {query}")
            response = requests.get(f"{base_url}?query={query}")
            request_count += 1  

            if response.status_code == 429:
                print(f"Rate limit hit. Retrying after {delay}s...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                continue

            response.raise_for_status()  
            data = response.json()
            
            for name in data.get("results", []):
                unique_names.add(name)
            
            return  # Exit after successful request
        
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error for query '{query}': {err}")
            break
        except requests.exceptions.RequestException as err:
            print(f"Request failed for query '{query}': {err}")
            time.sleep(2)  

# Function to generate queries
def generate_queries():
    for length in range(1, 3):  
        for chars in product(char_list, repeat=length):
            yield "".join(chars)

# Main script
print("Starting the script...")
for query in generate_queries():
    query_api(query)
    time.sleep(0.2)  # Increase delay to prevent 429 errors

# Save results
with open("names.txt", "w") as file:
    for name in unique_names:
        file.write(f"{name}\n")

print(f"Total unique names: {len(unique_names)}")
print(f"Total Requests Made: {request_count}")
print(f"Saved {len(unique_names)} names to names.txt")
print("Script completed.")
