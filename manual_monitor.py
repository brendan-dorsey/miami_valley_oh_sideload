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

    data_rows = soup.findAll("tr", { "class" : "dxgvDataRow" })

    # print data_rows
    # print len(data_rows)
    # print type(data_rows)

    # for i, row in enumerate(data_rows):
    #     print i + 1
    #     print type(row)
    #     print row.contents
    #     print "length: ", len(row.contents)
    #     print ""
    #     for i, tag in enumerate(row.contents):
    #         print i
    #         print tag.string
    #         print ""
    #     break

    incidents_array = []
    for i, row in enumerate(data_rows):
        incident = {}
        row_data = row.contents
        if len(row_data) < 9:
            continue

        incident["timestamp"] = row_data[2].string
        incident["id"] = "montgomery_county_oh_pd_" + row_data[3].string
        incident["headline"] = row_data[4].string
        location = row_data[6].string[:-4] + ", OH"
        location = location.replace("/", " and ")
        location = location.replace("PK", "PIKE")
        location = location.replace("BL", "BLVD")
        incident["location"] = location

        incidents_array.append(incident)

    # print incidents_array

    for item in incidents_array:
        print item["location"]

    print incidents_array







def single_query(link, payload):
    response = requests.get(link, params=payload)
    if response.status_code != 200:
        print 'WARNING', response.status_code
    else:
        return response.json()


if __name__ == '__main__':
    main()
