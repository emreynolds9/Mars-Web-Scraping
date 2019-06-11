from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create a function to execute all of your scraping code from above and
# return one Python dictionary containing all of the scraped data

def scrape():
    browser = init_browser()
    mars_dict = {}

    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html=browser.html
    soup_news = bs(html,'html.parser')
    news_title = soup_news.find('div',class_="content_title").find('a').get_text(strip=True)
    news_img = soup_news.find('div',class_="content_title")
    news_img = "https://mars.nasa.gov"+soup_news.find('img',class_="img-lazy")["data-lazy"]
    news_p = soup_news.find('div',class_="article_teaser_body").text
    
    browser = webdriver.Chrome()
    browser.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    elm = browser.find_element_by_xpath('//*[@id="full_image"]')
    elm.click()
    time.sleep(5)
    feat_img_url=browser.find_element_by_class_name('fancybox-image').get_attribute('src')
    browser.close()

    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    soup_twitter = bs(requests.get(url_twitter).text,'html.parser')
    mars_weather = soup_twitter.find('div',class_="js-tweet-text-container").find('p').get_text(strip=True)

    url_facts = 'https://space-facts.com/mars'
    tables = pd.read_html(url_facts)
    df=tables[0]
    df.columns = ['Characteristic', 'Fact']
    html_table = df.to_html(header=False,index=False).replace('\n', '')
    html_table = html_table.replace('\n', '')

    mars_dict = {
    "news_title": news_title,
    "news_p":news_p,
    "news_img":news_img,
    "feat_img_url":feat_img_url,
    "mars_weather":mars_weather,
    "html_table":html_table}
    # "hemi_data":hemi_data}

    browser.close

    return mars_dict


