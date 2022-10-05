# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:07:48 2022

@author: davim
"""


    
    
import os 
os.chdir("C:/Users/davim/Onedrive/Desktop")

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


import csv # we prefer csv over pandas to ensure that the memory of Python will not be saturated 
# by the important amount of data 

url = "https://www.tripadvisor.com/Restaurants-g187147-c8-Paris_Ile_de_France.html"

number_of_time = 36 # number of pages that we will scrape (not restaurants, but pages referencing restaurants)

class_page = "Lwqic.Cj.b"
class_next = "nav.next.rndBtn.ui_button.primary.taLnk"
class_expand = "taLnk.ulBlueLinks" # to expand the commentaires 


class_name = "HjBfq"
class_geo = "AYHFM"
class_title = "noQuotes"
class_text = "partial_entry"
class_date = "ratingDate"
class_note_gen = "ZDEqb"


"""
Retrieve the reviews from a webpage
"""
def get_data(driver_page, csv_writer, class_name, class_date, class_geo, class_title, class_text, class_note_gen):
        
    name =  driver_page.find_element(By.CLASS_NAME, class_name).get_attribute('innerText')
    geo = driver_page.find_element(By.CLASS_NAME, class_geo).get_attribute('innerText')
    date = driver_page.find_elements(By.CLASS_NAME, class_date)
    title = driver_page.find_elements(By.CLASS_NAME, class_title)
    text = driver_page.find_elements(By.CLASS_NAME, class_text)
    note = driver_page.find_element(By.CLASS_NAME, class_note_gen).get_attribute('innerText').replace('Â', '')
    for i in range(0, len(title)-1):
        csv_writer.writerow([name, date[i].get_attribute('innerText'), note, geo, title[i].get_attribute('innerText'), text[i].get_attribute('innerText').replace("\n", ". ")])


"""
Navigate from review page to next review page
"""
def retrieve_review(driver_page, csv_writer, class_name, class_date, class_geo, class_note_gen, class_title, class_text):

    get_data(driver_page, csv_writer, class_name, class_date, class_geo, class_title, class_text, class_note_gen)
        
    
    try: # if current page is the last
        while len(driver_page.find_elements(By.CLASS_NAME, "ui_button.nav.next.primary.disabled"))==0:  # we need to click on the "next" button to reach all reviews
            get_data(driver_page, csv_writer, class_name, class_date, class_geo, class_title, class_text, class_note_gen)
            driver_page.find_element(By.CLASS_NAME, "ui_button.nav.next.primary").click()
            
            # if current page is not the last 
        if (len(driver_page.find_elements(By.CLASS_NAME, "ui_button.nav.next.primary.disabled"))!=0):
            get_data(driver_page, csv_writer, class_name, class_date, class_geo, class_title, class_text, class_note_gen)
            
            # if current page is the unique
    except: pass

        

"""
Navigate from restaurant page to the next
"""
def get_reviews_tripadvisor(url, number_of_time, class_page, class_next):
    
    csv_file = open("reviews.csv", "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter = '|')
    csv_writer.writerow(['Café name', 'Date', 'General Grade', 'Geo location', 'Title', 'Review'])
    
    
    driver = webdriver.Chrome()
    driver.get(url)
    
    sleep(2) # to pause the system the time it loads
    
    # to deal with the pop-up for cookies 
    if driver.find_elements(By.ID, "onetrust-reject-all-handler"):
        driver.find_element(By.ID, "onetrust-reject-all-handler").click()
        sleep(1)

    
    i = 1
    
    while i < number_of_time:
        
        # first, we click on seel all
        
        #driver.find_element(By.CLASS_NAME, "ui_link").click()
        
        links = driver.find_elements(By.CLASS_NAME, class_page)
        assert len(links) != 0
    
        for j in range(len(links)):
            
            try:
                print(j)
                # go to the new page 
                links[j].click()
                sleep(1)
                # New tabs will be the last object in window_handles
                driver.switch_to.window(driver.window_handles[-1])
                
                if "https://www.tripadvisor.com/ShowUserReviews" in driver.current_url:
                    driver.close()
                else:
                    sleep(1)
                    driver.find_element(By.CLASS_NAME, class_expand).click() 
                    sleep(1)
                        # Retrieve the relevant data
                    try: 
                        retrieve_review(driver, csv_writer, class_name, class_date, class_geo, class_note_gen, class_title, class_text)
                        
                    except: 
                        pass
                        # close the tab
                    driver.close()
                        # switch to the main window
                    driver.switch_to.window(driver.window_handles[0]) 
                    sleep(1)
                
            except:
                pass


        # go to next page 
        driver.switch_to.window(driver.window_handles[0]) # because it needs it 
        driver.find_element(By.CLASS_NAME, class_next).click()
        
        i+=1
        sleep(2)
        
        csv_file.close()
        del csv_file
        del csv_writer
    

#%%% 

"""
Let's give it a try !

"""

get_reviews_tripadvisor(url, number_of_time, class_page, class_next)




