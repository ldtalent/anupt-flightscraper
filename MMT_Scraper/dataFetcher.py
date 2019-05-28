
# Required module imports
import csv
import selenium.webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# User defined variables for data retreival
origin = "BOM" 				# Origin airport code
destin = "DEL" 				# Destination airport code
trDate = "30/05/2019"		# Date for which data to be extracted.

""" The following is the Base Url for fetching data from MakeMyTrip Website.
	This URL appears in the search bar after origin, destination and date inputs on the landing page.
	Thus, this URL can be changed based on User Inputs and required data can be fetched.
"""
baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary="+ origin +"-"+ destin +"-"+ trDate +"&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E"

try:
	driver = selenium.webdriver.Chrome() # Chrome driver is being used.
	print ("Requesting URL: " + baseDataUrl)

	driver.get(baseDataUrl)  			 # URL requested in browser.
	print ("Webpage found ...")

	element_xpath = '//*[@id="left-side--wrapper"]/div[2]' # First box with relevant flight data.

	# Wait until the first box with relevant flight data appears on Screen
	element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

	# Scroll the page till bottom to get full data available in the DOM.
	print ("Scrolling document upto bottom ...")
	for j in range(1, 100):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# Find the document body and get its inner HTML for processing in BeautifulSoup parser.
	body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

	print("Closing Chrome ...") # No more usage needed.
	driver.quit() 				# Browser Closed.

	print("Getting data from DOM ...")
	soupBody = BeautifulSoup(body) # Parse the inner HTML using BeautifulSoup

	# Extract the required tags 
	spanFlightName = soupBody.findAll("span", {"class": "airways-name "}) 		# Tags with Flight Name
	pFlightCode = soupBody.findAll("p", {"class": "fli-code"})					# Tags with Flight Code
	divDeptTime = soupBody.findAll("div", {"class": "dept-time"})				# Tags with Departure Time
	pDeptCity = soupBody.findAll("p", {"class": "dept-city"})					# Tags with Departure City
	pFlightDuration = soupBody.findAll("p", {"class": "fli-duration"})			# Tags with Flight Duration
	pArrivalTime = soupBody.findAll("p", {"class": "reaching-time append_bottom3"}) # Tags with Arrival Time
	pArrivalCity = soupBody.findAll("p", {"class": "arrival-city"})				# Tags with Arrival City
	spanFlightCost = soupBody.findAll("span", {"class": "actual-price"})		# Tags with Flight Cost

	
	# Data Headers
	flightsData = [["flight_name", "flight_code", "departure_time", "departure_city", "flight_duration", "arrival_time", "arrival_city", "flight_cost"]]

	# Extracting data from tags and appending to main database flightsData
	for j in range(0, len(spanFlightName)):
		flightsData.append([spanFlightName[j].text, pFlightCode[j].text, divDeptTime[j].text, pDeptCity[j].text, pFlightDuration[j].text, pArrivalTime[j].text, pArrivalCity[j].text, spanFlightCost[j].text])

	# Output File for FlightsData. This file will have the data in comma separated form.
	outputFile = "FlightsData_" + origin +"-"+ destin +"-"+ trDate.split("/")[0] + "-" + trDate.split("/")[1] + "-" + trDate.split("/")[2] + ".csv"
	
	# Publishing Data to File
	print("Writing flight data to file: "+ outputFile + " ...")
	with open(outputFile, 'w', newline='') as spfile:
	    csv_writer = csv.writer(spfile)
	    csv_writer.writerows(flightsData)
	    print ("Data Extracted and Saved to File. ")

except Exception as e:
	print (str(e))


# EOF
# ----------------------------------------------------------------------------------------------------------
#print("Records\nFlight Name: "+ str(len(spanFlightName)) + "\nFlightCode: "+ str(len(pFlightCode)) + "\nDept Time: "+ str(len(divDeptTime)) + "\nDept City: "+ str(len(pDeptCity)) + "\nFlight Duration: "+ str(len(pFlightDuration)) + "\nArrival Time: "+ str(len(pArrivalTime)) + "\nArrival City: "+ str(len(pArrivalCity)) + "\nFlight Cost: "+ str(len(spanFlightCost)))
#print(flightsData)
#print(outputFile)

