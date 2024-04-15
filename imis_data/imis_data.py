import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests
# from pandas import DataFrame as df
from bs4 import BeautifulSoup
import re

chrome_options= Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
browser.get("https://imis.hib.gov.np/Default.aspx")

input_area = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.ID, "btnLogin"))
)

username_input = browser.find_element(By.ID, "txtUserName")
password_input = browser.find_element(By.ID, "txtPassword")
username_input.send_keys("sarita.gautam")
password_input.send_keys("Sarita@47")
login_button = browser.find_element(By.ID, "btnLogin")
login_button.click()

response = requests.get("https://imis.hib.gov.np/AutoCompleteHandlers/AutoCompleteHandler.ashx?_=1706267067891")
if response.status_code == 200:
    main_dg_data = response.json()

    for icd in main_dg_data:
        icd['ICDCode'] = icd.pop('ICDID')
        match = re.match(r'^(\S+)\s(.+)$', icd["ICDNames"])
        if match:
            icdcode = match.group(1)
            icdname = match.group(2)
        
        icd['ICDCode'] = icdcode
        icd['ICDNames'] = icdname
        

    with open("main_dg_data.json","w") as json_file:
        json.dump(main_dg_data, json_file,indent=4)

    print("data inserted successfully.") 

claim_link = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.ID,"Header_lblClaimsLink"))
)

claim_link.click()

health_facility_claims = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.ID,"Header_SubClaimOverview"))
)
health_facility_claims.click()

claim_administor = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.ID,"Body_ddlClaimAdmin"))
)
droupdown_select = Select(claim_administor)

droupdown_select.select_by_value("1180")

add_button = browser.find_element(By.ID, "Body_B_ADD")
add_button.click()

# service_input= WebDriverWait(browser, 10).until(
#     EC.presence_of_element_located((By.ID,"Body_gvService_txtServiceCode_0"))
# )
# service_input.click()

# service_div = browser.find_element(By.ID,"sugServPanel")
# service = service_div.find_element(By.ID,"DropDownSugTable").get_attribute("outerHTML")

# soup = BeautifulSoup(service, 'html.parser')

# # Find all rows in the table (skip the header row)
# rows = soup.select('tbody tr')[1:]

# # Extract data from each row
# service_data = {'Code': [], 'Name': [], 'Price': []}
# for row in rows:
#     columns = row.find_all('td')
#     service_data['Code'].append(columns[0].get_text(strip=True))
#     service_data['Name'].append(columns[1].get_text(strip=True))
#     service_data['Price'].append(columns[2].get_text(strip=True))

# with open("service_data.json","w") as service_file:
#     json.dump(service_data,service_file,indent=4)
#     print("service_data file created")

item_input= WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID,"Body_gvItems_txtItemCode_0"))
)
item_input.click()




item_div = browser.find_element(By.ID,"sugServPanel")
items = item_div.find_element(By.ID,"DropDownSugTable").get_attribute("outerHTML")

soup = BeautifulSoup(items, 'html.parser')

# Find all rows in the table (skip the header row)
rows = soup.select('tbody tr')[1:]

# Extract data from each row
item_data = {'Code': [], 'Name': [], 'Price': []}
for row in rows:
    columns = row.find_all('td')
    item_data['Code'].append(columns[0].get_text(strip=True))
    item_data['Name'].append(columns[1].get_text(strip=True))
    item_data['Price'].append(columns[2].get_text(strip=True))

with open("item_data.json","w") as item_file:
    json.dump(item_data,item_file,indent=4)
    print("item_data file created")
