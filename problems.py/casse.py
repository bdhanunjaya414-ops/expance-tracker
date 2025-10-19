import requests
from bs4 import BeautifulSoup

# Example endpoint (replace with actual eCourts endpoint from Network tab)
URL = "https://anantapur.dcourts.gov.in/case-status-search-by-case-number/"

# Example payload for POST request (adjust according to form fields)
payload = {
    "case_type": "Civil",
    "case_number": "25",
    "case_year": "2025",
    "court_code": "",        # optional
    "date": "14-10-2025"     # for cause list
}

# Optional headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

# Send POST request
response = requests.post(URL, data=payload, headers=headers)

# Check response
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")  # cause list is usually in a table
    if table:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            serial = cols[0].text.strip()
            court_name = cols[1].text.strip()
            case_no = cols[2].text.strip()
            case_type = cols[3].text.strip()
            print(f"{serial}: {court_name} - {case_type} {case_no}")
else:
    print("Error fetching data:", response.status_code)
