from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

# Start by converting your Jupyter notebook into a Python script called scrape_mars.py 
# with a function called scrape that will execute all of your scraping code from above 
# and return one Python dictionary containing all of the scraped data.
def scrape():
    browser = init_browser()
    url_news = 'https://mars.nasa.gov/news/'
    soup_news = bs(requests.get(url_news).text,'html.parser')
    news_title = soup_news.find('div',class_="content_title").find('a').get_text(strip=True)
    # news_img = soup_news.find('div',class_="content_title")
    news_img = "https://mars.nasa.gov"+soup_news.find('img',class_="img-lazy")["data-lazy"]
    news_p = soup_news.find_all('div',class_="content_title")[0].get_text(strip=True)
    browser = webdriver.Chrome()
    browser.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    elm = browser.find_element_by_xpath('//*[@id="full_image"]')
    elm.click()
    time.sleep(5)
    feat_img_url=browser.find_element_by_class_name('fancybox-image').get_attribute('src')
    print(feat_img_url)
    browser.close()
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    soup_twitter = bs(requests.get(url_twitter).text,'html.parser')
    mars_weather = soup_twitter.find('div',class_="js-tweet-text-container").find('p').get_text(strip=True)
    url_facts = 'https://space-facts.com/mars'
    tables = pd.read_html(url_facts)
    df=tables[0]
    df.columns = ['Characteristic', 'Fact']
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    html_table
    mars_facts_table = df.to_html('table.html')
    mars_data = {
    "news_title": news_title,
    "news_p":news_p,
    "mars_weather":mars_weather,
    "mars_facts_table":mars_facts_table}

    return mars_data

