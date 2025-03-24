# AutoComplete API Scraper

## Overview
This script extracts all possible names from an autocomplete API (`http://35.200.185.69:8000/v3/autocomplete`). Since the API is undocumented, we explore its behavior and constraints through systematic querying.

## Features
- Generates query strings using **letters (a-z), digits (0-9), and special characters (+, -, space, .)**.
- Implements **exponential backoff** for handling `429 Too Many Requests` errors.
- Extracts and stores unique names from the API responses.
- Saves the extracted names to `names.txt`.

## Tools Used: POSTMAN (for exploration)
## How It Works
1. **Query Generation:**
   - Generates queries of length 1 and 2 using all valid characters.
   - Uses `itertools.product` to create all possible combinations.

2. **API Request Handling:**
   - Sends a GET request to the API with the generated query.
   - Handles rate limits (`429` errors) using exponential backoff (retrying with increasing delays).
   - Extracts names from the JSON response and stores them in a set.

3. **Execution:**
   - Queries are executed with a **0.2-second delay** between requests.
   - Results are saved in `names.txt`.

## Installation
Ensure you have Python installed, then install dependencies:
```sh
pip install requests
```

## Usage
Run the script:
```sh
python script.py
```

## Output
- Extracted names are stored in `names.txt`.
- Console output shows progress, request count, and rate limit handling.

## Challenges & Solutions
- **Rate Limiting:** Implemented exponential backoff to retry failed requests.
- **Efficient Querying:** Limited query length to optimize API calls.

## Results
# For `http://35.200.185.69:8000/v1/autocomplete`
- **Total requests made:** `718`
- **Total unique names extracted:** `6720`
# For `http://35.200.185.69:8000/v2/autocomplete`
- **Total requests made:** `1435`
- **Total unique names extracted:** `7705`
# For `http://35.200.185.69:8000/v3/autocomplete`
- **Total requests made:** `1714`
- **Total unique names extracted:** `7729`

## Future Improvements
- Implement parallel requests with controlled throttling.
- Use caching to avoid redundant queries.
- Extend query length dynamically based on response patterns.

# Author
**Harish Nandre**
