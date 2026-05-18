from bs4 import BeautifulSoup
import requests
import sys
import csv

def parse_arguments() -> tuple[str, str]:
    """
    Validates command-line arguments.

    Returns:
        tuple[str, str]: (url, csv_filename)
    """
    if len(sys.argv) != 3:
        print("to run the program, enter two arguments, url address and csv file")
        sys.exit(1)

    url = sys.argv[1]
    csv_file = sys.argv[2]

    if not url.startswith("https://"):
        print("invalid url")
        sys.exit(1)

    if not csv_file.lower().endswith(".csv"):
        print("The second argument must be a CSV file.")
        sys.exit(1)

    return url, csv_file

def download_page(url: str) -> BeautifulSoup:
    """
    Downloads the HTML page and returns a BeautifulSoup object.

    Parameters:
        url (str): URL to download.

    Returns:
        BeautifulSoup: Parsed HTML of the page.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print("invalid url")
            sys.exit(1)

    except requests.exceptions.RequestException:
        print("The URL is not accessible.")
        sys.exit(1)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def extract_municipalities(soup: BeautifulSoup) -> list[dict[str, str]]:
    """
    Extracts all municipalities from the district page (ps32).

    Parameters:
        soup (BeautifulSoup): Parsed HTML of the district page.

    Returns:
        list[dict[str, str]]:
            A list of municipalities where each municipality contains:
            {
            "url": municipality detail URL,
            "code": municipality code,
            "location": municipality name
            }
    """
    municipalities = []
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    tables = soup.find_all("table")

    for table in tables:
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            a_tag = cols[0].find("a")
            if not a_tag:
                continue
            if not a_tag.text.isdigit():
                continue
            full_url = base_url + a_tag.get("href")

            one_municipality = {
                "url": full_url,
                "code": a_tag.text.strip(),
                "location": cols[1].text.strip()
            }
            municipalities.append(one_municipality)
    return municipalities

def extract_voters(soup: BeautifulSoup) -> dict[str, str]:
    """
    Extract voter statistics (registered, envelopes, valid votes) from a ps311 page.

    Parameters:
        soup (BeautifulSoup): Parsed HTML of the ps311 results page.

    Returns:
        dict[str, str]: Dictionary containing:
            {
                "registered": "...",
                "envelopes": "...",
                "valid": "..."
            }
    """
    table = soup.find("table", id="ps311_t1")
    if not table:
        print("Statistics table not found.")
        sys.exit(1)

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 8:
            continue
        voters_set = {
            "registered": cols[3].text.strip().replace("\xa0", ""),
            "envelopes": cols[4].text.strip().replace("\xa0", ""),
            "valid": cols[7].text.strip().replace("\xa0", "")
            }
        return voters_set
    return {}

def extract_results(soup: BeautifulSoup) -> dict[str, str]:
    """
    Extract results statistics (party name → votes) from a ps311 page.

    Parameters:
        soup (BeautifulSoup): Parsed HTML of the ps311 results page.

    Returns:
        dict[str, str]: Dictionary containing:
            {
            "party": "votes"
            }
    """
    results = {}
    all_tables = soup.find_all("table", class_="table")
    for table in all_tables:
        if table.get("id") == "ps311_t1":
            continue

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            party = cols[1].text.strip()
            votes = cols[2].text.strip()
            if party == "-" and votes == "-":
                continue

            results[party] = votes
    return results

def save_to_csv(final_data, csv_file) -> None:
    """Save election data into a CSV file."""
    if not final_data:
        print("No data to save.")
        return

    headers = final_data[0].keys()

    with open(csv_file, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file,
                                fieldnames=headers,
                                delimiter=";")

        writer.writeheader()
        for row in final_data:
            writer.writerow(row)

def main():
    url, csv_file = parse_arguments()
    district_soup = download_page(url)
    municipalities = extract_municipalities(district_soup)
    final_data = []

    for municipality in municipalities:
        print("Processing:", municipality["location"])
        one_row = {}

        detail_soup = download_page(municipality["url"])
        voters = extract_voters(detail_soup)
        results = extract_results(detail_soup)

        one_row.update(municipality)
        one_row.pop("url")
        one_row.update(voters)
        one_row.update(results)
        final_data.append(one_row)

    save_to_csv(final_data, csv_file)

if __name__ == "__main__":
    main()