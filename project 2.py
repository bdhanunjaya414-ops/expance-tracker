import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import click
from datetime import datetime, timedelta

BASE_URL = "https://ecourts.gov.in/"  # Placeholder: replace with actual eCourts API or URL

def fetch_case(cnr=None, case_type=None, number=None, year=None, day="today"):
    """
    Fetch case details from eCourts.
    """
    # Calculate date
    if day.lower() == "today":
        date = datetime.now().strftime("%d-%m-%Y")
    elif day.lower() == "tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    else:
        raise ValueError("day must be 'today' or 'tomorrow'")
    
    # Build query URL (example, needs real eCourts API)
    params = {
        "cnr": cnr,
        "case_type": case_type,
        "case_number": number,
        "case_year": year,
        "date": date
    }
    
    response = requests.get(BASE_URL + "case_status", params=params)
    
    if response.status_code != 200:
        print("Error fetching data")
        return None

    # Parse HTML (assuming HTML table response)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")  # eCourts usually lists in tables
    
    cases = []
    if table:
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cols = row.find_all("td")
            case_info = {
                "serial_number": cols[0].text.strip(),
                "court_name": cols[1].text.strip(),
                "case_number": cols[2].text.strip(),
                "case_type": cols[3].text.strip(),
                "date": date
            }
            cases.append(case_info)
    
    return cases

def save_results(cases, filename="cases.json"):
    with open(filename, "w") as f:
        json.dump(cases, f, indent=4)
    print(f"Results saved to {filename}")

@click.command()
@click.option("--cnr", default=None, help="CNR number")
@click.option("--case_type", default=None, help="Case type")
@click.option("--number", default=None, help="Case number")
@click.option("--year", default=None, help="Case year")
@click.option("--day", default="today", help="Day to check: today or tomorrow")
@click.option("--save", is_flag=True, help="Save output to JSON file")
def main(cnr, case_type, number, year, day, save):
    cases = fetch_case(cnr, case_type, number, year, day)
    if not cases:
        print("No cases found.")
        return

    print("Cases Found:")
    for case in cases:
        print(f"{case['serial_number']}: {case['court_name']} - {case['case_type']} {case['case_number']}")

    if save:
        save_results(cases)

if __name__ == "__main__":
    main()
