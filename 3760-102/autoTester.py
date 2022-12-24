from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.chrome.options import Options #
#from selenium.webdriver.support.select import Select #
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import pandas as pd


def launchBrowser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://34.130.154.243')
    return driver


# Tests if data returned in table on website matches XML data
def testSearch(driver, data, input):
    # Type "cis3760" to search bar & click search button
    searchButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchButton"]')))
    searchBar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="courseCode"]')))
    searchBar.send_keys(input)
    searchButton.click()

    # Read table
    table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainText"]/table')))
    tableStr = table.text

    # Parse data from testcases.json
    dumped = json.dumps(data["testcase1"])
    output = []
    jsonData = data["testcase1"]
    loaded = json.loads(dumped)
    keys = ['name', 'term', 'meetings', 'faculty', 'status']
    i = 0
    for x in jsonData:
      values = x.values()
      string = ""
      for y in keys:
        string = string + loaded[i][y] + " "
        string = string.replace("\n", " ")
      string.strip()
      output.append(string)
      i += 1
    testData = "\n".join(output)

    testData = testData.replace(" ", "")
    testData = testData.replace("\n", "")
    tableStr = tableStr.replace(" ", "")
    tableStr = tableStr.replace("\n", "")

    searchBar.clear() # Clear search bar

    # Assert test condition
    assert testData == tableStr, "Did not match"


# Tests if changing the semester on the website returns the corresponding semester data
def testSemester(driver, sem):
  # Select semester from drop-down
  selectDropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="semDropDown"]')))
  selectDropdown.click()
  if (sem == "F22"):
    selectSem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search"]/div/div/div[1]/div[1]/div/a[1]')))
  else:
    selectSem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search"]/div/div/div[1]/div[1]/div/a[2]')))
  selectSem.click()

  # Input course to search
  searchButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchButton"]')))
  #searchBar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="courseCode"]')))
  #searchBar.send_keys("mgmt3020")
  searchButton.click()

  # Read term from table
  time.sleep(0.5)
  term = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainText"]/table/tbody/tr[1]/td[2]')))

  searchBar.clear() # Clear search bar
  searchBar.clear() # Clear search bar
  
  # Assert test condition
  if sem == "F22":
    assert "Fall" in term.text, "Semester did not match"
  elif sem == "W23":
    assert "Winter" in term.text, "Semester did not match"


# Testing if the days off drop-down selector returns classes with no meeting times on specified days
def testDaysOff(driver, numDaysOff):
  # Select days off drop-down
  selectDODropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dayDropDown"]')))
  selectDODropdown.click()
  if numDaysOff == 1: # Select one day off (Monday)
    selectDay = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]')))
    selectDay.click()
  else: # Select two days off (Tuesday & Thursday)
    selectDODropdown.click()
    selectDay1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="2"]')))
    selectDay2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="4"]')))
    selectDay1.click()
    selectDay2.click()

  # Click search button
  searchButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchButton"]')))
  searchButton.click()
  time.sleep(0.5) # Wait for table to load
 
  # Read meeting times from table and load into Pandas dataframe
  table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainText"]/table')))
  html = driver.page_source
  table = pd.read_html(html)
  df = table[0]
  meetings = df.loc[:,2]

  # Count meeting times in table that don't include the day off
  count = 0
  for i in meetings:
    if numDaysOff == 1:
      if ("Mon" not in i) or ("LAB TBA" in i and "LEC TBA" in i) or ("Distance Education" in i):
        count += 1
    else:
      if ("Tues" not in i and "Thurs" not in i) or ("LAB TBA" in i and "LEC TBA" in i) or ("Distance Education" in i):
        count += 1

  # Unclick days off
  selectDODropdown.click()
  if numDaysOff == 1:
    selectDay.click()
  else: # Select two days off (Tuesday & Thursday)
    selectDay1.click()
    selectDay2.click()

  # If the number of classes without a meeting time on the specified day = the total number of classes on
  # the list, the test case passes
  assert count == meetings.shape[0], "Count did not match"




# MAIN
# Read in test cases
with open('testcases.json', 'r') as f:
  data = json.load(f)
driver = launchBrowser()

# Tests
print("--- Search Tests ---")
testSearch(driver, data, "cis3760")
print("Test 1 passed (Course-level search) - \"cis3760\"")
testSearch(driver, data, "acct")
print("Test 2 passed (Faculty-level search) - \"acct\"")

# Input course to search
searchBar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="courseCode"]')))
searchBar.clear()
searchBar.clear()
searchBar.send_keys("mgmt3020")

print("--- Semester Tests ---")
testSemester(driver, "F22")
print("Test 3 passed (Semester check) - \"F22\"")
testSemester(driver, "W23")
print("Test 4 passed (Semester check) - \"W23\"")

# Input faculty to search
searchBar.clear()
searchBar.send_keys("phys")

print("--- Days Off Tests ---")
testDaysOff(driver, 1)
print("Test 6 passed (Days Off Check) - Monday off")
testDaysOff(driver, 2)
print("Test 6 passed (Days Off Check) - Tuesday & Thursday off")


driver.close()

