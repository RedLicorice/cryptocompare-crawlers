from scrapers import SocialStatsScraper
from symbols import SymbolManager
from dotenv import load_dotenv
import os

#Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

if __name__ == "__main__":
	appName = os.environ.get("APP_NAME")
	apiKey = os.environ.get("API_KEY")
	startDt = os.environ.get("START_DATE")
	endDt = os.environ.get("END_DATE")
	symbols = os.environ.get("SYMBOLS").split(",")
	SymbolManager.loadData(os.environ.get("SYMBOLS_DATA"))
	for sym in symbols:
		ss = SocialStatsScraper(appName, apiKey, startDt, endDt, sym) # End date is excluded
		if ss.run():
			ss.save(os.environ.get("OUTDIR"))