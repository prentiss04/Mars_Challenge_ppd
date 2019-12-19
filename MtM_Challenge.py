#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import re

# Set the executable path and initialize the chrome browsewr in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

html = browser.html
hemi_soup = BeautifulSoup(html, 'html.parser')

#create list for Hemisphere content
hemi_list =[]

for i in range (0,4): #(len(hemi_titles_list)):
    # visit splash page
    #html = browser.html
    #hemi_soup = BeautifulSoup(html, 'html.parser')
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Get the hemisphere title with splinter
    hemi_titles_list = browser.find_by_css('.description .itemLink')
    hemi_title = hemi_titles_list[i].value
    print(hemi_title)

    # Parse the resulting html with soup
    #hemi_soup = BeautifulSoup(html, 'html.parser')
    #hemi_ext_links = hemi_soup.select('.description .itemLink', wait_time=2)
    hemi_splinter_link = browser.find_by_css('div.description a.itemLink')

    hemi_splinter_links = hemi_splinter_link[i]["href"]

    # generate new url and visit page
    #new_img_url = f'https://astrogeology.usgs.gov{hemi_splinter_links}'
    #print(new_img_url)
    browser.visit(hemi_splinter_links)
    #print(i) # remove later

    # scrape site for high-res image
    img_soup = BeautifulSoup(html, 'html.parser')
    #high_res_suffix = img_soup.select_one('img.wide-image')#, wait_time=2)
    sample_example = browser.find_link_by_text('Sample').first
    #print(i) # remove later
    #print(high_res_suffix)
    #print(sample_example)
    sample_img = sample_example["href"]
    print(sample_img)

    # create dictionary pair
    hemi_pair = {'Title': hemi_title, 'Image': sample_img}
    print(hemi_pair)

    # append hemi_list with new dictionary content
    hemi_list.append(dict(hemi_pair))
    print(hemi_list)