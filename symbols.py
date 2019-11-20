import json

class SymbolManager:
	data = None

	@classmethod
	def loadData(cls, filename):
		if not cls.data:
			with open(filename, "r")as fp:
				wrapped = json.load(fp)
				cls.data = wrapped["Data"]

	@classmethod
	def getId(cls, symbol):
		if not cls.data:
			raise EnvironmentError("No data loaded")
		if not symbol in cls.data:
			raise ValueError("No data found for symbol {}".format(symbol))
		return cls.data[symbol]["Id"]

	@classmethod
	def getName(cls, symbol):
		if not cls.data:
			raise EnvironmentError("No data loaded")
		if not symbol in cls.data:
			raise ValueError("No data found for symbol {}".format(symbol))
		return cls.data[symbol]["CoinName"]