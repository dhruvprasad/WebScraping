"""A module to find minerals."""

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import time

# Collect a user input to crawl minerals.net for minerals of
# the user specified letter
print("Enter letter: ")
user_input = input()
site_name = "http://www.minerals.net/Minerals/{}.aspx"
letter_choice = rq.get(site_name.format(user_input))
soup_choice = BeautifulSoup(letter_choice.text, "html.parser")
 
minerals_a = []
data_table = soup_choice.find('div', {"id": "ctl00_ContentPlaceHolder1_one"})
# row_one_all = data_table.find_all("tr")[0] #first row
for row_one_all in data_table.find_all("tr"):
    row_one_minerals = row_one_all.find_all('div', {'id': lambda x: x and x.endswith('_divMineral')})
    for each_mineral in row_one_minerals:
        links = each_mineral.find('a')
        title = links.get('href')
        minerals_a.append(title)

def loop(key, value, dt_row, dicta):
    """Take key, value, row and dict, accumulate values to dict and return."""
    chem_name = dt_row.find('span', {"id": value})
 
    if chem_name:
        dicta[key] = "N/A"
    else:
        dicta[key] = chem_name.text
    return dicta
 
absurd_name = "ctl00_ContentPlaceHolder1_lblCrystalFormsandAggregates"

THING = {"Chemical Formula": "ctl00_ContentPlaceHolder1_lblChemicalFormula",
         "Composition": "ctl00_ContentPlaceHolder1_lblComposition",
         "Color": "ctl00_ContentPlaceHolder1_lblColor",
         "Streak": "ctl00_ContentPlaceHolder1_lblStreak",
         "Hardness": "ctl00_ContentPlaceHolder1_lblHardness",
         "Crystal System": "ctl00_ContentPlaceHolder1_lblCrystalSystem",
         "Crystal Forms and Aggregates": absurd_name,
         "Transparency": "ctl00_ContentPlaceHolder1_lblTransparency",
         "Luster": "ctl00_ContentPlaceHolder1_lblLuster",
         "Cleavage": "ctl00_ContentPlaceHolder1_lblCleavage",
         "Fracture": "ctl00_ContentPlaceHolder1_lblFracture",
         "Tenacity": "ctl00_ContentPlaceHolder1_lblTenacity",
         "In Group": "ctl00_ContentPlaceHolder1_lblInGroup",
         "Striking Features": "ctl00_ContentPlaceHolder1_lblStrikingFeatures",
         "Environment": "ctl00_ContentPlaceHolder1_lblEnvironment",
         "Popularity": "ctl00_ContentPlaceHolder1_lblPopularity",
         "Prevalence": "ctl00_ContentPlaceHolder1_lblPrevalence",
         "Demand": "ctl00_ContentPlaceHolder1_lblDemand"}

all_minerals = []

for mineral in minerals_a:
    print('I am fetching: {}'.format(mineral))
    name = rq.get("http://www.minerals.net/" + mineral)
    print(name.text)
    time.sleep(1)
    soup_name = BeautifulSoup(name.text, "html.parser")
    dt = soup_name.find('div', {"id": "ctl00_ContentPlaceHolder1_one"})
    dt_row = dt.find_all("tr")[4]
    dicta = {}

    # print(mineral)
    # TODO: Write some code for walking DOM tree
    for k, v in THING.items():
        loop(k, v, dt_row, dicta)

    all_minerals.append(dicta)

 

pd.DataFrame(all_minerals).to_csv("minerals.csv", index=None)
