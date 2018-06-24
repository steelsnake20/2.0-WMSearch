class SearchResult:

	def __init__(self, storeName, strainName, price, webURL, city, closingTime, rating):
		self.storename = storeName
		self.strainName = strainName
		self.price = price
		self.webURL = webURL
		self.city = city
		self.closingTime = closingTime
		self.rating = rating

	def getStoreName(self):
		return self.storename
	def getStrainName(self):
		return self.strainName;
	def getPrice(self):
		return self.price
	def getWebURL(self):
		return self.webURL
	def getCity(self):
		return self.city
	def getClosingTime(self):
		return self.closingTime
	def getRating(self):
		return self.rating
