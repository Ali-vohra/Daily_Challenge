from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os
import glob
from selenium.webdriver.common.keys import Keys
import pyautogui
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import re
import random

time.sleep(5)
        
##def popup(driver,default_handle):
##        handles = list(driver.window_handles)
##        if len(handles) > 1:
##                handles.remove(default_handle)
##                while len(handles) > 0:
##                        driver.switch_to_window(handles[0])
##                        driver.close()
##        driver.switch_to_window(default_handle)

configParser = configparser.RawConfigParser()   
configFilePath = "C:\\Users\\SONY\\script.ini"
configParser.read(configFilePath, encoding='utf-8-sig')

##settings = {
##    "recentDestinations": [
##        {
##            "id": "Save as PDF",
##            "origin": "local",
##            "account": ""
##        }
##    ],
##    "selectedDestinationId": "Save as PDF",
##    "version": 2
##}
##
##profile = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}

chrome_options = webdriver.ChromeOptions()
##chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--start-maximized')

chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs

chrome_prefs["profile.default_content_settings"] = { "popups": 1 }

username = configParser.get('credentials','username')
password = configParser.get('credentials','password')
url = 'https://brilliant.org/daily-problems/'
url1 = 'https://brilliant.org/'

PATH = "C:\\Users\\SONY\\Downloads\\chromedriver_win32\\chromedriver.exe"

driver = webdriver.Chrome(options = chrome_options, executable_path = PATH)

default_handle = driver.current_window_handle

wait = WebDriverWait(driver, 10)

driver.get(url1)
##popup(driver,default_handle)

log_in = wait.until(lambda driver:driver.find_element(By.LINK_TEXT, "Log in"))
log_in.click()

log_in_google = wait.until(lambda driver:driver.find_element(By.CLASS_NAME, 'btn.google'))
log_in_google.click()

sign_in = wait.until(lambda driver:driver.find_element(By.ID, 'identifierId'))
sign_in.send_keys(username)

next_btn = wait.until(lambda driver:driver.find_element(By.ID, 'identifierNext'))
next_btn.click()

time.sleep(2)
pass_word = wait.until(lambda driver:driver.find_element(By.NAME, 'password'))
pass_word.send_keys(password)

next_btn1 = wait.until(lambda driver:driver.find_element(By.ID, 'passwordNext'))
next_btn1.click()

##popup(driver,default_handle)
all_elements = wait.until(lambda driver:driver.find_elements(By.CLASS_NAME, 'dp-feed-item'))
all_elements[0].click()

meta_h = wait.until(lambda driver:driver.find_element_by_class_name('b-title-meta'))
section_h = wait.until(lambda driver:driver.find_element_by_class_name('b-title-section'))

file_name = re.sub(r'[\\/*?:"<>|]',"",'Problem_' + meta_h.text + '_' + section_h.text)
filename = re.sub(r'[\\/*?:"<>|]',"",file_name + '.html')

keep_reading = wait.until(lambda driver:driver.find_element_by_id('dp-expand'))
keep_reading.click()

top = wait.until(lambda driver:driver.find_element_by_id('header'))
driver.execute_script("arguments[0].setAttribute('style','display:none')", top)
time.sleep(1)

side = wait.until(lambda driver:driver.find_element_by_id('cmp_daily_problems_sidebar_id'))
driver.execute_script("arguments[0].setAttribute('style','display:none')", side)

time.sleep(2)
pyautogui.hotkey('ctrl', 's')
time.sleep(1)
pyautogui.typewrite(filename)
time.sleep(1)
pyautogui.hotkey('enter')

time_to_wait = 120
time_counter = 0
while not os.path.exists('C:\\Users\\SONY\\Downloads\\' + filename):
    time.sleep(1)
    time_counter += 1
    if time_counter > time_to_wait:
            break
shutil.move('C:\\Users\\SONY\\Downloads\\' + filename, 'E:\\version-control\\Brilliant\\' + filename)

source = 'C:\\Users\\SONY\\Downloads\\' + file_name + '_files'
dest = 'E:\\version-control\\Brilliant\\' + file_name + '_files'

files = os.listdir(source)
os.mkdir(dest)
time.sleep(1)

for f in files:
        shutil.move(source + '\\' + f, dest + '\\')

time.sleep(2)
os.rmdir(source)

##driver.execute_script('window.print();')
##time.sleep(7)

##list_of_files = glob.glob('C:\\Users\\SONY\\Downloads\\*.pdf')
##latest_file = max(list_of_files, key=os.path.getctime)
##os.rename(latest_file,file_name)

int_ans = 3
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
#answer = wait.until(lambda driver:driver.find_element_by_id('id_answer'))
#answer.send_keys(int_ans)
length = len(driver.find_elements_by_css_selector("label[class='choice btn btn-mcq']"))
##length = len(driver.find_elements_by_css_selector("label[class='choice btn btn-mcq btn-multi-select']"))
(wait.until(lambda driver:driver.find_elements_by_css_selector("label[class='choice btn btn-mcq']")))[random.randrange(0,length)].click()
##(wait.until(lambda driver:driver.find_elements_by_css_selector("label[class='choice btn btn-mcq btn-multi-select']")))[random.randrange(0,length)].click()

submit = wait.until(lambda driver:driver.find_element_by_link_text("Submit"))
submit.send_keys(Keys.ENTER)
##popup(driver,default_handle)

file_name_1 = re.sub(r'[\\/*?:"<>|]',"",'Solution_' + meta_h.text + '_' + section_h.text)
filename1 = re.sub(r'[\\/*?:"<>|]',"",file_name_1 + '.html')

time.sleep(1)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(1)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
##driver.execute_script('window.print();')
##time.sleep(5)

pyautogui.hotkey('ctrl', 's')
time.sleep(1)
pyautogui.typewrite(file_name_1 + '.html')
pyautogui.hotkey('enter')

time_to_wait = 120
time_counter = 0
while not os.path.exists('C:\\Users\\SONY\\Downloads\\' + filename1):
    time.sleep(0.5)
    time_counter += 1
    if time_counter > time_to_wait:
            break
shutil.move('C:\\Users\\SONY\\Downloads\\' + filename1, 'E:\\version-control\\Brilliant\\' + filename1)

source = 'C:\\Users\\SONY\\Downloads\\' + file_name_1 + '_files'
dest = 'E:\\version-control\\Brilliant\\' + file_name_1 + '_files'

files = os.listdir(source)
os.mkdir(dest)
time.sleep(1)
for f in files:
        shutil.move(source + '\\' + f, dest + '\\')
time.sleep(2)
os.rmdir(source)

##list_of_files_1 = glob.glob('C:\\Users\\SONY\\Downloads\\*.pdf')
##latest_file_1 = max(list_of_files_1, key=os.path.getctime)
##os.rename(latest_file_1,file_name_1)   

driver.close()
print("Successfully Completed")
driver.quit()
