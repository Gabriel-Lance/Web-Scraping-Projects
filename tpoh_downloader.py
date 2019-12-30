"""
A web scraper that automatically downloads every page of a web comic called The Property of Hate

The pages will be saved to a directory named TPoH, which will be created in the program's directory.  Any pages
that have already been downloaded will be skipped.
"""

import requests
import os
import pickle
from bs4 import BeautifulSoup as bs

last_url_file_name = ".\\tpoh_last_url.p"

# If a file of the last URL visited is found, the program begins scraping from there.
if os.path.isfile(last_url_file_name):
    with open(last_url_file_name, "rb") as pfile:
        url = pickle.load(pfile)
# If there is no file of the last URL visited, the program begins at the first page
else:
    url = "http://www.thepropertyofhate.com/TPoH/The%20Hook/1"

while True:
    # Downloads the web page
    req = requests.get(url, headers={"User-agent": "Chrome"})
    req.raise_for_status()
    req_soup = bs(req.text, features="html.parser")

    # Gets the number and chapter of the current page, which is used to name the file
    title = req_soup.select("div.comic_title")[0].text
    chapter, page = title.split(" : ")

    page_path = os.path.join("TPoH", f"{page} ({chapter}).jpg")

    # Downloads the image if it hasn't already been downloaded
    if not os.path.isfile(page_path):
        print(f"Downloading {title}")
        img_url = "http://thepropertyofhate.com" + req_soup.select("div.comic_comic > img")[0]["src"]
        img_file = requests.get(img_url, headers={"User-agent": "Chrome"})
        img_file.raise_for_status()
        with open(page_path, "wb") as file:
            for chunk in img_file.iter_content(100000):
                file.write(chunk)
    else:
        print(f"{title} already exists")

    # Gets the URL pointed to by the "next" button, which will be used on the next loop to download the next image
    # If there is no "next" button, next_button will be an empty list, which will cause an IndexError that signals the
    # end of the comic
    try:
        next_button = req_soup.select("a[title='Next']")[0]
        next_link = next_button.get("href").split()
        url = "http://thepropertyofhate.com" + "%20".join(next_link)
    except IndexError:
        break

# Saves the last URL visited to be used the next time the program is run
with open(last_url_file_name, "wb") as pfile:
    pickle.dump(url, pfile)

print("Done!")
