from pymongo import MongoClient
import requests
from os import environ
from bs4 import BeautifulSoup
import time


def main():
    # Initiate mongo client
    client = MongoClient()
    # Initiate Database
    db = client["test_database"]
    # Initiate Table
    coll = db["test_coll"]

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
        location = location.replace("/", " and ")
        location = location.replace("PK", "PIKE")
        location = location.replace("BL", "BLVD")
        incident["location"] = location

        # Add incident to output array
        incidents_array.append(incident)

    return incidents_array


if __name__ == '__main__':
    print main()
