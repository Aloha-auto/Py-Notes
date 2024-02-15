# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 15:04:20 2024

@author: Alois
"""

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import ftplib
import re
import os


USER = os.environ['USER'] #mondossierweb
PASS = os.environ['PASS'] #mondossierweb
FTP_HOST = os.environ['FTP_HOST']
FTP_USER = os.environ['FTP_USER']
FTP_PASS = os.environ['FTP_PASS']
FTP_DIR = os.environ['FTP_DIR']
PDF_URL = os.environ['PDF_URL'] #custom
subject = os.environ['subject'] #ntfy Notes
test_subject = os.environ['test_subject'] #ntfy test


requests.post(f"https://ntfy.sh/{test_subject}", data="Notes is running")


t1 = time.time()

def merge_lists(list_one, list_two):
    result = []
    length = min(len(list_one), len(list_two))
    for i in range(length):
        result.append((list_one[i], list_two[i]))
    return result

def remove_doublons(liste):
    if liste[-1] == liste[-2]:
        liste.pop(-1)
        remove_doublons(liste)
        
def remove_beginning_recoverage(end_result):
    for i in range(1, len(end_result)):
        stop = False
        while stop == False:
            if end_result[i][0] in end_result[i-1]:
                end_result[i].pop(0)
            else :
                stop = True
                
def remove_end_recoverage(end_results):
    for i in range(1, len(end_result)):
        j = len(end_result[i]) - 1
        stop = False
        while j > 0 and stop == False:
            if end_result[i][j] in end_result[i-1]:
                end_result[i].pop(j)
                j -= 1
            else :
                stop = True

def remove_end_recoverage2(end_results):
    for i in range(1, len(end_result)):
        stop = False
        while stop == False:
            if end_result[i][-1] in end_result[i-1]:
                end_result[i].pop(-1)
            else :
                stop = True
    
def merge_end_result(end_result):
    res = []
    for liste in end_result :
        res += liste
    return res

t1 = time.time()

firefox_options = Options()
# firefox_options.add_argument("-headless")

display = False
file = True

### INIT
counter = 1
initiated = False
while not initiated and counter < 5:
    try:
        driver = webdriver.Firefox()
        initiated = True
    except:
        print(f"Couldn't start browser, trying again... ({counter})")
        counter += 1
        time.sleep(1)
if counter == 5 :
    raise Exception("Couldn't start browser after 5 attempts, exiting program...")
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

buttons = []

while buttons == []:
    buttons = driver.find_elements(By.XPATH, "//vaadin-button[text()='Notes et résultats']")
    time.sleep(2)
# button = driver.find_elements(By.XPATH, "/html/body/vaadin-app-layout/vaadin-vertical-layout[2]/vaadin-vertical-layout/vaadin-vertical-layout[1]/vaadin-vertical-layout/vaadin-vertical-layout/div[2]/div[2]/vaadin-button")

buttons[0].click()

    


end_result = []

old_text = "empty"
new_text = ""

while old_text != new_text :
    old_text = new_text
    g = []
    
    time.sleep(1)
    new_text = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
    time.sleep(1)
    
    lines = new_text.split('style="---level: ')
    lines.pop(0)
    
    for el in lines :
        level = el[0]
        title =  re.findall('(?<=<div style="white-space: normal; flex-grow: 1;">).*?(?=<\/div>)', el)[0]
        note = re.findall('(?<=<div style="margin: auto; font-size: smaller; font-style: italic;">).*?(?=<\/div>)|(?<=<div style="margin: 0.1em auto 0.1em 1em; width: 5em; height: 1.5em;">).*?(?=\/20<\/div>)', el)[0]
        g.append([level, title, note])
    
    end_result.append(g)
    
    # list_element = driver.find_element(By.XPATH, "/html/body/vaadin-dialog-overlay/div/vaadin-vertical-layout/vaadin-grid")
    list_element = driver.find_element(By.TAG_NAME, "vaadin-grid")
    
    ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()
    ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()
    # ActionChains(driver).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).scroll_from_origin(ScrollOrigin(list_element, 10, 10), 0, 100000).perform()
    
    time.sleep(2)
                
time.sleep(1)
driver.close()

remove_doublons(end_result)
remove_end_recoverage(end_result)
remove_beginning_recoverage(end_result)

final_result = merge_end_result(end_result)

def find_path(notes, indice):
    path = []
    i = indice
    level = int(notes[i][0])
    lowest = level # + 1 # pour inclure la matiere dans le path
    while i > 0 and level != 0 :
        level = int(notes[i][0])
        if level < lowest:
            path.insert(0, notes[i][1])
            lowest = level
        i -= 1
    return path

def trouver_differences(old_notes, new_notes):
    differences = []
    while(len(old_notes) < len(new_notes)):
        for i in range(len(new_notes)):
            if new_notes[i] not in old_notes:
                differences.append({"matiere": new_notes[i][1], "path": find_path(new_notes, i), "old": None, "new": new_notes[i][2]})
                old_notes.insert(i, new_notes[i])
    for i in range(len(new_notes)):
        if old_notes[i] != new_notes[i]:
            differences.append({"matiere": new_notes[i][1], "path": find_path(new_notes, i), "old": old_notes[i][2], "new": new_notes[i][2]})
    return differences


### FTP

# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"

ftp.sendcmd(f"CWD {FTP_DIR}")

filename = "string.json"
with open(filename, "wb") as file:
    # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {filename}", file.write)

with open(filename, 'r') as f :
    old = json.load(f)
    
if final_result != old:
    with open(filename, 'w') as f :
        json.dump(final_result, f)
    with open(filename, "rb") as file:
        # use FTP's STOR command to upload the file
        ftp.storbinary(f"STOR {filename}", file)
    print("diff")
    d = trouver_differences(old, final_result)
    # print(d)
    for el in d :
        try :
            if float(el["new"]) >= 12 : tag, news = "green_book", "Cool !"
            elif float(el["new"]) >= 9 : tag, news = "blue_book", "Ok..."
            else : tag, news = "orange_book", "Pas dingue"
        except :
            tag, news = "grey_question", "Pas d'info"
        r = requests.post(f"https://ntfy.sh/{subject}", data=f"{news}\n\n\n{el['matiere']} : {el['new']}".encode(encoding='utf-8'), headers={"Title": "Nouvelle note", "Tags": tag, "Priority": "2", "Actions": f"view, PDF, {PDF_URL}, clear=true"})
        if r.status_code == "200":
            print("Notified!")
else :
    print("no diff")

t2 = time.time()

print(f"Code ran in {t2 - t1} seconds")
