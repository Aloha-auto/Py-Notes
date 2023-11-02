# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 15:33:24 2023

@author: Alois
"""

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import json
import os

USER = os.environ['USER'] #mondossierweb
PASS = os.environ['PASS'] #mondossierweb
URL = os.environ['URL'] #jsonbin
API_KEY = os.environ['API_KEY'] #jsonbin
PDF_URL = os.environ['PDF_URL'] #custom
subject = os.environ['subject'] #ntfy Notes
test_subject = os.environ['test_subject'] #ntfy test

requests.post(f"https://ntfy.sh/{test_subject}", data="Notes is running")

firefox_options = Options()
firefox_options.add_argument("-headless")

display = False
file = True
pdf = True

### INIT
driver = webdriver.Firefox(options=firefox_options)

### AUTH

driver.get("https://login.insa-lyon.fr/cas/login?service=https%3A%2F%2Fmondossierweb.insa-lyon.fr%2Fmondossierweb%2Flogin%2Fcas")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys(USER)
password.send_keys(PASS)


time.sleep(1)

password.submit()

time.sleep(1)



### GET_CONTENT

driver.get("https://mondossierweb.insa-lyon.fr/mondossierweb/inscriptions")

# button = driver.find_elements(By.TAG_NAME, "vaadin-button")

buttons = driver.find_elements(By.XPATH, "//vaadin-button[text()='Notes et résultats']")

buttons[0].click()

time.sleep(1)

cells = driver.find_elements(By.TAG_NAME, "vaadin-grid-cell-content")

while len(cells) < 40:
    cells = driver.find_elements(By.TAG_NAME, "vaadin-grid-cell-content")
    

matiere, note, level = "", "", ""

if file :
    dic = {}
 

for cell in cells :
    if len(cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")) > 0 :
        matiere, level, note = "", "", ""
        level = cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")[0].value_of_css_property("---level")
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            matiere = cell.find_elements(By.TAG_NAME, "div")[1].text
    elif len(cell.find_elements(By.TAG_NAME, "flow-component-renderer")) > 0 :
        note = ""
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            note = cell.find_elements(By.TAG_NAME, "div")[1].text
    if matiere and note :
        if display :
            print("Level : " + level + " / Matiere : " + matiere + " / Note : " + note)
        if file :
            if level == "0":
                dic[matiere] = {"level": level, "note": note}
                semestre = matiere
            elif level == "2":
                dic[semestre][matiere] = {"level": level, "note": note}
                ue = matiere
            elif level == "3":
                dic[semestre][ue][matiere] = {"level": level, "note": note}

def trouver_differences(dic1, dic2, parent_keys=None):
    if parent_keys is None:
        parent_keys = []

    differences = []

    for key in dic1:
        if key in dic2:
            if isinstance(dic1[key], dict) and isinstance(dic2[key], dict):
                sub_differences = trouver_differences(dic1[key], dic2[key], parent_keys + [key])
                differences.extend(sub_differences)
            elif key == "note" and dic1[key] != dic2[key]:
                difference = {
                    "semestre": parent_keys[0] if parent_keys else None,
                    "ue": parent_keys[1] if len(parent_keys) > 1 else None,
                    "matiere": parent_keys[-1],
                    "old": dic1[key],
                    "new": dic2[key],
                }
                differences.append(difference)
        else:
            difference = {
                "semestre": parent_keys[0] if parent_keys else None,
                "ue": parent_keys[1] if len(parent_keys) > 1 else None,
                "matiere": parent_keys[-1],
                "old": dic1[key] if key in dic1 else None,
                "new": dic2[key] if key in dic2 else None,
            }
            differences.append(difference)

    for key in dic2:
        if key not in dic1:
            difference = {
                "semestre": parent_keys[0] if parent_keys else None,
                "ue": parent_keys[1] if len(parent_keys) > 1 else None,
                "matiere": key,
                "old": None,
                "new": dic2[key],
            }
            differences.append(difference)

    return differences

old = requests.get(URL, headers={"authorization": f"token {API_KEY}"}).json()
if dic != old :
    requests.post(URL, data = json.dumps(dic), headers={"authorization": f"token {API_KEY}"})
    d = trouver_differences(old, dic)
    print(d)
    for el in d :
        if int(el["new"]) >= 12 : tag = "green_book"
        elif int(el["new"]) >= 9 : tag = "blue_book"
        else : tag = "orange_book"
        if pdf :
            requests.post(f"https://ntfy.sh/{subject}", data=f"{el['matiere']} : {el['new']}", headers={"Title": "Nouvelle note", "Tags": tag, "Actions": f"view, PDF, {PDF_URL}, clear=true"})
        else :
            requests.post(f"https://ntfy.sh/{subject}", data=f"{el['matiere']} : {el['new']}", headers={"Title": "Nouvelle note", "Tags": tag})
