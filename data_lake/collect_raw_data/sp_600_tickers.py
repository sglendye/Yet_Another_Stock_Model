import requests
from bs4 import BeautifulSoup
import sys
import json

class RawTable:
    ''' This is the table of the ticker data '''
    def __init__(self, url):
        self.url = url
        self.results = requests.get(self.url)
        self.soup = BeautifulSoup(self.results.content, 'html.parser')
    
    def init_table(self):
        # Tickers are stored in a table on the page tagged as constituents
        self.table = self.soup.find("table", {"id": "constituents"})

    # Header for the table columns
    def table_header(self):
        self.header = []
        head_row = self.table.find_all('th')
        for value in head_row:
            self.header.append(value.text.rstrip("\n")) # Stripping the tag for new line. They're frequently leftover in wiki
        
    # Content of the  table columns
    def table_content(self):
        self.content = []
        # Cells are nested in td values within table rows. Need to break it down by looping over each row and then each value in each row
        content_rows = self.table.find_all('tr')
        for row in content_rows:
            ticker = [] # Storing the rows as separate lists for easy parsing
            for value in row.find_all('td'):
                ticker.append(value.text.rstrip("\n"))
            self.content.append(ticker)
    
    def jsonify(self):
        # Using our header to generate key value pairs for each of the rows by looping through the elements and matching them up
        self.json = []
        head_length = len(self.header)
        for row in self.content:
            content_length = len(row)
            if head_length == content_length:
                company = dict.fromkeys(self.header, 0)
                for i in range(head_length):
                    company[self.header[i]] = row[i]
                self.json.append(company)

    def store_json(self):
        with open(r'C:/Users/swgle/Desktop/Stock Modeling/lake/s & p 600 stocks.json', 'w') as fout:
            json.dump(self.json , fout)


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_600_companies'
table = RawTable(url)
table.init_table()
table.table_header()
table.table_content()
table.jsonify()
table.store_json()
