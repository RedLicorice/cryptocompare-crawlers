from cryptocompare import SocialStatsScraper
from googletrends import GoogleTrendsScraper
from symbols import SymbolManager
from dotenv import load_dotenv
import os
import sys

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
		if 'social' in sys.argv:
			ss = SocialStatsScraper(appName, apiKey, startDt, endDt, sym) # End date is excluded
			if ss.run():
				ss.save(os.environ.get("OUTDIR"))
			else:
				print("Failed to scrape social stats")
	if 'trends' in sys.argv:
		searchTerms = os.environ.get("TRENDS_TERMS")
		if not searchTerms:
			terms = symbols + [SymbolManager.getName(s) for s in symbols if SymbolManager.getName(s) != s]
		else:
			terms = searchTerms.split(",")
		stateFile = os.environ.get("TRENDS_STATEFILE")
		gs = GoogleTrendsScraper()
		if os.path.exists(stateFile) and os.stat(stateFile).st_size > 0:
			state = gs.load_state(stateFile)
		else:

			state = gs.build_state(startDt, endDt, terms)
			gs.save_state(state,stateFile)
		gs.run(state)