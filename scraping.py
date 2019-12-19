#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import datetime
import re

def scrape_all():
    # initiate headless driver for deployment
    # Set the executable path and initialize the chrome browsewr in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in directory
    mars_data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(browser),
            "mars_hemispheres": mars_hemis(browser),
            #"mars_hemispheres": mars_hemis(browser),
            # "image_url": actual_url
            # "title_url": actual_title       #uncomment this when ready!!!
            "last_modified": datetime.now()
    }
    print(mars_data)
    return mars_data
    #browser.quit()

# Save as scraping.py

def mars_news(browser):

    # Set the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')


    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # using the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
            return None, None

    return news_title, news_p


def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the fill image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

# try without the "try" block

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    #return img_url_rel

    # try:
    #     # Find the relative image url
    #     img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    #     return img_url_rel

    # except AttributeError:
    #     return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

# should i not include "browser" in the mars_facts fxn?
def mars_facts(browser):
    #df = pd.read_html('https://space-facts.com/mars/')[0]
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://space-facts.com/mars/')[0]

    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars']
    #df.columns=['description', 'Mars', "Earth"]
    #df.columns=['description', 'Value']
    df.set_index('description', inplace=True)
    # Convert data frame into HTML format, add bootstrap
    return df.to_html(classes="table")

###########################################################################################
# High-res image fxn

def mars_hemis(browser):

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)

    #html = browser.html
    #hemi_soup = BeautifulSoup(html, 'html.parser')

    #create list for Hemisphere content
    hemi_list = []

    for i in range (0,4): #(len(hemi_titles_list)):
        # visit splash page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # Get the hemisphere title with splinter
        hemi_titles_list = browser.find_by_css('.description .itemLink')
        hemi_title = hemi_titles_list[i].value
        #print(hemi_title)

        # Parse the resulting html with soup
        hemi_splinter_link = browser.find_by_css('div.description a.itemLink')

        hemi_splinter_links = hemi_splinter_link[i]["href"]

        # generate new url and visit page
        browser.visit(hemi_splinter_links)

        # scrape site for high-res image
        #img_soup = BeautifulSoup(html, 'html.parser')
        sample_example = browser.find_link_by_text('Sample').first
        sample_img = sample_example["href"]
        #print(sample_img)

        # create dictionary pair
        hemi_pair = {'Title': hemi_title, 'Image': sample_img}
        #print(hemi_pair)

        # append hemi_list with new dictionary content
        hemi_list.append(dict(hemi_pair))

        if i == 3:
            return (hemi_list)

# create the empty list before the function, return the dictionary pair, append them to the list with each loop interation


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

#<img src="{{mars.mars_hemis}}" class="img-responsive" alt="Responsive image">