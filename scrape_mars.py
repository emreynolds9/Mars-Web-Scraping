from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create a function to execute all of your scraping code from above and
# return one Python dictionary containing all of the scraped data

def scrape():
    now = datetime.datetime.now()
    date_time=now.strftime("%A, %B %d %Y %I:%m%p %Z")
    browser = init_browser()
    mars_dict = {}

    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html=browser.html
    soup_news = bs(html,'html.parser')
    #Title
    news_title = soup_news.find('div',class_="content_title").find('a').get_text(strip=True)
    #Image
    news_img = soup_news.find('div',class_="content_title")
    news_img = "https://mars.nasa.gov"+soup_news.find('img',class_="img-lazy")["data-lazy"]

    #Date
    news_date = soup_news.find('div',class_="image_and_description_container").find('div',class_='list_date').text
    #Paragraph Text
    news_p = soup_news.find('div',class_="image_and_description_container").find('div',class_="rollover_description_inner").text


    browser = webdriver.Chrome()
    browser.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    elm = browser.find_element_by_xpath('//*[@id="full_image"]')
    elm.click()
    time.sleep(5)
    feat_img_url=browser.find_element_by_class_name('fancybox-image').get_attribute('src')
    browser.close()

    # url_twitter = 'https://twitter.com/marswxreport?lang=en'
    # soup_twitter = bs(requests.get(url_twitter).text,'html.parser')
    # mars_weather = soup_twitter.find('div',class_="js-tweet-text-container").find('p').get_text(strip=True)

    url_facts = 'https://space-facts.com/mars'
    tables = pd.read_html(url_facts)
    df=tables[0]
    df.columns = ['Characteristic', 'Mars',"Earth"]
    html_table = df.to_html(header=True,index=False, classes='table table-striped').replace('\n', '')
    html_table = html_table.replace('\n', '')

    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    soup_hemi = bs(requests.get(url_hemi).text,'html.parser')
    hemisphere_data = []
    results = soup_hemi.findAll("a", {'class':['itemLink', 'product-item']})
    for result in results:
        end_link = result["href"]
        url_hemi_each = "https://astrogeology.usgs.gov"+end_link
        soup_hemi_each = bs(requests.get(url_hemi_each).text,'html.parser')
        img_url = soup_hemi_each.findAll("div",class_="downloads")[0].find("a")["href"]
        title = soup_hemi_each.findAll("div",class_="content")[0].find("h2").text
        hemisphere_data.append({"title":title,"img_url":img_url})

    mars_dict = {
    "date_time":date_time,
    "news_title": news_title,
    "news_p":news_p,
    "news_img":news_img,
    "news_date":news_date,
    "feat_img_url":feat_img_url,
    # "mars_weather":mars_weather,
    "html_table":html_table,
    "hemisphere_data":hemisphere_data}

    browser.close

    return mars_dict


