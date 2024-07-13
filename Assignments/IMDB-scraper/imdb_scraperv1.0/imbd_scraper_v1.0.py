
import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from itertools import chain
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# Function to extract cast names for movies from IMDB
def scrape_imdb_moviecasts(imdb_id):
    url = f"https://www.imdb.com/{imdb_id}/"

    # For bypassing the scrapper stopper by making it seem like the request is coming from a PC
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Capture the entire html file
    response = requests.get(url, headers=headers)
    cast_name_list=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Using data-test to extract 

        cast_prep=soup.find('section',attrs={"data-testid": "title-cast"})
        casts=cast_prep.find('div',attrs={"data-testid": "shoveler"})
        casts_names=casts.find('div',attrs={"data-testid": "shoveler-items-container"})
        cast_names_largelist=casts_names.find_all('div',attrs={"data-testid": "title-cast-item"})
        for names in cast_names_largelist:
            cast_name_list.append(names.text)
        return cast_name_list


def login():

    chrome_options = Options()
    chrome_options.add_argument("--windowsize=1920,1000")

    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the IMDb login page
    driver.get("https://www.imdb.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fregistration%2Fap-signin-handler%2Fimdb_us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS8_cmVmXz1sb2dpbiJ9&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&tag=imdbtag_reg-20")

    # Find the username and password fields and fill them in
    username_field = driver.find_element(By.XPATH,"//input[@id='ap_email']")
    password_field = driver.find_element(By.XPATH,"//input[@id='ap_password']")

    load_dotenv()

    username = os.getenv('username')
    password = os.getenv('pass')

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    # Time to fillin captcha otheriwise it will just wait 
    captcha_bypass()
    goto_watchlist(driver)
    print("Login Succesfull")
    return getlink_title(driver)

def goto_watchlist(driver):
    driver.get("https://www.imdb.com/user/ur182878039/watchlist/")

def getlink_title(driver):
    link_lists=[]
    page_source=driver.page_source
    watch_list = BeautifulSoup(page_source, 'html.parser')
    movies= watch_list.find('ul',class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jmWPOZ detailed-list-view ipc-metadata-list--base')
    movie_lists = movies.find_all('li',class_='ipc-metadata-list-summary-item')
    for link in movie_lists:
        temp=link.find('a')
        links=temp.get('href')
        link_lists.append(links)
    return (link_lists)

def captcha_bypass():
    time.sleep(15)
    pass

def login2():
    url='https://accounts.evernote.com/login'
    chrome_options = Options()
    chrome_options.add_argument("--windowsize=1920,1000")

    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the IMDb login page
    driver.get(f"{url}")

    time.sleep(3)

    # Find the username and password fields and fill them in
    username_field = driver.find_element(By.XPATH,"//input[@id='email']")

    username_field.send_keys('Lord')
    time.sleep(30)

def proceed():
    last_list=[]
    link_list=login()
    print(link_list)
    for link in link_list:
        last_list.append((scrape_imdb_moviecasts(link)))
    table_creation(last_list)

def table_creation(nested_list):
    flattened_list = list(chain.from_iterable(nested_list))
    df = pd.DataFrame(flattened_list, columns=['Actors'])
    frequency = df['Actors'].value_counts().reset_index()
    frequency.columns = ['Actors', 'Frequency']
    print(frequency)
    csv_filename = 'actor_frequency.csv'
    frequency.to_csv(csv_filename, index=False)

proceed()
