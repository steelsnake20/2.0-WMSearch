import requests
import json
import operator
import SearchResult
import sys

# The main list to store all of the search results.
searchResults = []

def main():
	url = getUrlForDispensaryListings()
	printMenu()
	weedAmount = getUserMenuChoice()
	showLoadingMessage()
	buildSearchResults(url, weedAmount)
	sortAndPrintResults()
	printMessageIfNoResults()

def buildUrlFor(location):
	url = "https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D="
	url += location
	url += "&page_size=100&size=100"
	return url

def getUrlForDispensaryListings():
	if(len(sys.argv) > 1):
		if(sys.argv[1] == "peninsula"):
			return buildUrlFor("the-penisula")
		return buildUrlFor(sys.argv[1])
	return buildUrlFor("san-francisco")
	
def printMenu():
	print("1. eighth")
	print("2. quarter")
	print("3. half_ounce")
	print("4. ounce")

def getUserMenuChoice():
	desiredAmount = input("How much weed? (1-4): ")
	validateMenuChoice(desiredAmount)
	weedAmount = "eighth"
	if desiredAmount == "2":
		weedAmount = "quarter"
	elif desiredAmount == "3":
		weedAmount = "half_ounce"
	elif desiredAmount == "4":
		weedAmount = "ounce"
	return weedAmount

def validateMenuChoice(menuChoice):
	while menuChoice != "1" and menuChoice != "2" and menuChoice != "3" and menuChoice != "4":
		printMenu()
		menuChoice = input("How much weed? (1-4): ")

def buildSearchResults(mainURL, weedAmount):
	allDispensaries = requests.get(mainURL).json()
	for dispensary in allDispensaries["data"]["listings"]:

		dispensaryName = dispensary["name"]
		city = dispensary["city"]
		dispensaryRequestUrl = buildWebUrlForDispensary(dispensary)

		# Make a request to the individual dispensary
		dispensaryData = requests.get(dispensaryRequestUrl).json()

		openStatus = dispensaryData["listing"]["todays_hours"]["open_status"]
		closingTime = dispensaryData["listing"]["todays_hours"]["closing_time"]
		licenseType = dispensaryData["listing"]["license_type"]
		rating = dispensaryData["listing"]["rating"]

		# Traverse through all of the menu items for the individual dispensary
		for menuItems in dispensaryData["categories"]:
			for item in menuItems["items"]:
				categoryName = item["category_name"]
				strainName = item["name"]
				if categoryName == "Indica" or categoryName == "Sativa" or categoryName == "Hybrid":
					price = item["prices"][weedAmount]
					url = "https://weedmaps.com" + item["url"]
					if isValidItem(price, openStatus, licenseType, strainName.lower()):
						result = SearchResult.SearchResult(dispensaryName, strainName, price, url, city, closingTime, rating)
						searchResults.append(result)

def isValidItem(price, openStatus, licenseType, strainName):
	if price > 3.0 and price != 420 and openStatus != "CLOSED" and licenseType != "medical" and "budlets" not in strainName and "shake" not in strainName and "trim" not in strainName:
		return True
	return False

def buildWebUrlForDispensary(dispensary):
	url = "https://api-g.weedmaps.com/wm/web/v1/listings/"
	url += dispensary["web_url"].rsplit('/', 1)[-1]
	url += "/menu?type=delivery"
	return url

def sortAndPrintResults():
	sortedWeedItems = sorted(searchResults, key=operator.attrgetter('price'), reverse=True)
	for item in sortedWeedItems:
		print("Price: $" + str(item.getPrice()))
		print("Strain:",item.getStrainName())
		print("Dispensary:",item.getStoreName())
		print("City:",item.getCity())
		print("Closing time:",item.getClosingTime())
		print("Rating: " + str("{:,.2f}".format(item.getRating())) + " out of 5")
		print("URL:",item.getWebURL())
		print()

def printMessageIfNoResults():
	if len(searchResults) <= 0:
		print()
		print("No results.")
		print("This could be because there are no recreational dispensaries in the given area, or none are open.")

def showLoadingMessage():
	print("Loading results... This may take 20 - 30 seconds.")

main()

