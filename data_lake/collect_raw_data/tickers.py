import json

class StockTicker:
    def __init__(self, stocks):

        self.data = open(stocks)
        self.data = json.load(self.data)

    def collect_tickers(self):
        self.tickers = []
        for i in self.data:
            self.tickers.append(i['Ticker symbol'])

stocks = r'C:/Users/swgle/Desktop/Stock Modeling/Data Lake/s & p 600 stocks.json'
data = StockTicker(stocks)
data.collect_tickers()

print(data.tickers)