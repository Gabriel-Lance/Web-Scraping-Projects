import requests
from bs4 import BeautifulSoup as bs
from openpyxl import Workbook

url = "http://quotes.toscrape.com"
wb = Workbook()
ws = wb.active
ws["A1"].value = "Quote"
ws["B1"].value = "Author"
ws["C1"].value = "Tags"
current_row = 2
while True:
    current_page = bs(requests.get(url).text, "html.parser")
    quote_blocks = current_page.select("div[class='quote']")
    for quote_block in quote_blocks:
        quote = quote_block.select("span[class='text']")[0].text
        author = quote_block.select("span > small[class='author']")[0].text
        tags = [tag.text for tag in quote_block.select("a[class='tag']")]
        print("Quote: " + quote)
        print("Author: " + author)
        print("Tags: " + str(tags))
        ws.cell(row=current_row, column=1).value = quote
        ws.cell(row=current_row, column=2).value = author
        ws.cell(row=current_row, column=3).value = ", ".join(tags)
        current_row += 1
    try:
        url = "http://quotes.toscrape.com" + current_page.select("li[class='next']>a")[0]["href"]
    except IndexError:
        break

wb.save("quote_scrape.xlsx")
