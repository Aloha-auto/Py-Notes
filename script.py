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
FTP_HOST = os.environ['FTP_HOST']
FTP_USER = os.environ['FTP_USER']
FTP_PASS = os.environ['FTP_PASS']
PDF_URL = os.environ['PDF_URL'] #custom
subject = os.environ['subject'] #ntfy Notes
test_subject = os.environ['test_subject'] #ntfy test

requests.post(f"https://ntfy.sh/{test_subject}", data="Notes is running")

firefox_options = Options()
firefox_options.add_argument("-headless")

display = False
file = True

### INIT
driver = webdriver.Firefox(options=firefox_options)
# driver.set_window_size(1920,2000)

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

driver.get("https://mondossierweb.insa-lyon.fr/mondossierweb/inscriptions?continue")

# button = driver.find_elements(By.TAG_NAME, "vaadin-button")
time.sleep(5)

# a = input("wait")

buttons = driver.find_elements(By.XPATH, "//vaadin-button[text()='Notes et résultats']")
# button = driver.find_elements(By.XPATH, "/html/body/vaadin-app-layout/vaadin-vertical-layout[2]/vaadin-vertical-layout/vaadin-vertical-layout[1]/vaadin-vertical-layout/vaadin-vertical-layout/div[2]/div[2]/vaadin-button")

buttons[0].click()

time.sleep(1)

cells = driver.find_elements(By.TAG_NAME, "vaadin-grid-cell-content")

time.sleep(1)

    


dic = {}
    
matiere, note, level = None, None, None
 
passes = set()


for cell in cells:
    # print(cell.get_attribute("slot"))
    if len(cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")) > 0 :
        matiere, level, note = "", "", None
        level = cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")[0].value_of_css_property("---level")
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            matiere = cell.find_elements(By.TAG_NAME, "div")[1].text
    else :
        note = None
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            note = cell.find_elements(By.TAG_NAME, "div")[-1].text
            if note in {'Aucun résultat', '', None}:
                note = 'Aucun résultat'
            else :
                note = float(note[:-3])
    if matiere is not None and note is not None:
        if matiere not in passes :
            passes.add(matiere)
            if display :
                print("Level : " + level + " / Matiere : " + matiere + " / Note : " + str(note))
            if file :
                if level == "1":
                    dic[matiere] = {"level": level, "note": note}
                    semestre = matiere
                elif level == "3":
                    dic[semestre][matiere] = {"level": level, "note": note}
                    ue = matiere
                elif level == "4":
                    dic[semestre][ue][matiere] = {"level": level, "note": note}
                    ec = matiere
                elif level == "5":
                    dic[semestre][ue][ec][matiere] = {"level": level, "note": note}


list_element = driver.find_element(By.XPATH, "/html/body/vaadin-dialog-overlay/div/vaadin-vertical-layout/vaadin-grid")

ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()
ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()
ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()

time.sleep(2)

cells2 = driver.find_elements(By.TAG_NAME, "vaadin-grid-cell-content")

for cell in cells2:
    # print(cell.get_attribute("slot"))
    if len(cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")) > 0 :
        matiere, level, note = "", "", None
        level = cell.find_elements(By.TAG_NAME, "vaadin-grid-tree-toggle")[0].value_of_css_property("---level")
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            matiere = cell.find_elements(By.TAG_NAME, "div")[1].text
    else :
        note = None
        if len(cell.find_elements(By.TAG_NAME, "div")) > 0 :
            note = cell.find_elements(By.TAG_NAME, "div")[-1].text
            if note in {'Aucun résultat', '', None}:
                note = 'Aucun résultat'
            else :
                note = float(note[:-3])
    if matiere is not None and note is not None:
        if matiere not in passes :
            passes.add(matiere)
            if display :
                print("Level : " + level + " / Matiere : " + matiere + " / Note : " + str(note))
            if file :
                if level == "1":
                    dic[matiere] = {"level": level, "note": note}
                    semestre = matiere
                elif level == "3":
                    dic[semestre][matiere] = {"level": level, "note": note}
                    ue = matiere
                elif level == "4":
                    dic[semestre][ue][matiere] = {"level": level, "note": note}
                    ec = matiere
                elif level == "5":
                    dic[semestre][ue][ec][matiere] = {"level": level, "note": note}
                
time.sleep(1)
driver.close()

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


# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"

ftp.sendcmd('CWD files.aloha.42web.io/htdocs/protected/')

filename = "notes.json"
with open(filename, "wb") as file:
    # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {filename}", file.write)

with open(filename, 'r') as f :
    old = json.load(f)
    
if dic != old:
    with open(filename, 'w') as f :
        json.dump(dic, f)
    with open(filename, "rb") as file:
        # use FTP's STOR command to upload the file
        ftp.storbinary(f"STOR {filename}", file)
    print("diff")
    d = trouver_differences(old, dic)
    print(d)
    for el in d :
        if int(el["new"]) >= 12 : tag, news = "green_book", "Cool !"
        elif int(el["new"]) >= 9 : tag, news = "blue_book", "Ok..."
        else : tag, news = "orange_book", "Pas dingue"
        r = requests.post(f"https://ntfy.sh/{subject}", data=f"{news}\n\n\n{el['matiere']} : {el['new']}".encode(encoding='utf-8'), headers={"Title": "Nouvelle note", "Tags": tag, "Priority": "2", "Actions": "view, PDF, http://files.aloha.42web.io/protected/pdf.php, clear=true"})
        if r.status_code == "200":
            print("Notified!")
else :
    print("no diff")
