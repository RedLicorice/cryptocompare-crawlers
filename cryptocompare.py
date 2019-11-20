import requests
from datetime import datetime
import time
import csv
from symbols import SymbolManager
import os
from pytrends.request import TrendReq

class Scraper:
	results = []
	basename = 'scraper'

	def __init__(self, appName, apiKey, begin, end, symbol):
		self.appName = appName
		self.apiKey = apiKey
		self.symbol = symbol
		self.end = time.mktime(datetime.strptime(end, "%Y-%m-%d").timetuple())
		self.begin = time.mktime(datetime.strptime(begin, "%Y-%m-%d").timetuple())

	def save(self, dir = 'output'):
		filename = "{}_{}.csv".format(self.basename, self.symbol)
		if dir:
			os.makedirs(dir, True)
		filename = os.path.join(dir, filename)
		#Sort results by ascending time
		results = sorted(self.results, key = lambda x: x['time'])
		# Add a Date field for indexing
		for item in results:
			item.update({"Date": datetime.fromtimestamp(item["time"]).strftime("%Y-%m-%d")})
			del item["time"]
		# Save to CSV
		with open(filename, "w", newline='') as fp: # csv writer automatically adds newlines
			fields = ["Date"] + [k for k in results[0].keys() if k != "Date"]
			wr = csv.DictWriter(fp, delimiter=",", fieldnames=fields)
			wr.writeheader()
			wr.writerows(results)

class SocialStatsScraper(Scraper):
	basename = 'social'
	query = "https://min-api.cryptocompare.com/data/social/coin/histo/day?coinID={coinId}&aggregate=1&toTs={toTs}&api_key={api_key}"

	def run(self):
		timestamp = self.end
		symId = SymbolManager.getId(self.symbol)
		seen = []
		self.results = []
		while timestamp > self.begin:
			query = self.query.format(coinId=symId, toTs=timestamp, api_key=self.apiKey)
			r = requests.get(query)
			if r.status_code != 200:
				raise RuntimeError("Failed to get data for timestamp {}".format(timestamp))
			resp = r.json()
			seq = []
			# No regrets
			for item in resp["Data"]:
				# API returns 31 days so requests might overlap, prevent duplicates
				if item["time"] in seen:
					continue
				seen.append(item["time"])
				# Save item's timestamp to get min
				seq.append(item["time"])
				self.results.append(item)
			print("{}:{}| current: {} target: {}".format(self.basename, self.symbol, timestamp, self.begin))
			timestamp = min(seq)
			time.sleep(0.1) # at most 10 calls per second to avoid rate limiting
		return len(self.results)