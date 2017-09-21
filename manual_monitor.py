import requests
from bs4 import BeautifulSoup
import re


def main():
    # URL to scrape
    url = "http://www.montgomery.miamivalleydispatch.org/"

    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    # Collect all data rows from display table
    data_rows = soup.findAll("tr", {"class": "dxgvDataRow"})

    # Loop through data rows to build output array
    incidents_array = []
    for i, row in enumerate(data_rows):
        incident = {}
        row_data = row.contents

        # Control to ensure only filled rows are parsed
        if len(row_data) < 9:
            continue

        # Parse row data by position (html tags are common to all fields) and
        # update incident information with relevant data
        incident["timestamp"] = row_data[2].string
        incident["id"] = "montgomery_county_oh_pd_" + row_data[3].string
        incident["headline"] = row_data[4].string

        # Logic for interpreting location coding
        location = row_data[6].string[:-4] + ", OH"
        location = re.sub("/", " and ", location)
        location = re.sub(r"\bPK\b", r"PIKE", location)
        location = re.sub(r"\bBL\b", r"BLVD", location)
        location = re.sub(r"\bAV\b", r"AVE", location)
        location = re.sub("([0-9]+)[NSEW]B", r"-\1", location)
        incident["location"] = location

        # Add incident to output array
        incidents_array.append(incident)

    for item in incidents_array:
        print item["location"]

    return incidents_array


if __name__ == '__main__':
    print main()
