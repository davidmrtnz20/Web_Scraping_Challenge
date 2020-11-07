from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

executable_path = {'executable_path': '/Users/Milo/Downloads/chromedriver_win32/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    scraped_data = {}
    output = marsNews()
    scraped_data['mars_news'] = output[0]
    scraped_data['mars_article'] = output[1]
    scraped_data['mars_images'] = marsImages()
    scraped_data['mars_facts'] = marsFacts()
    scraped_data['mars_hemisphere'] = marsHemisphere()
    return scraped_data

def marsNews():
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')
    article = soup.find('div', class_="list_text")
    news_title = article.find('div', class_="content_title").text
    news_p = article.find('div', class_="article_teaser_body").text
    output = [news_title, news_p]
    return output

def marsImages():
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    images_html = browser.html
    soup = BeautifulSoup(images_html, 'html.parser')
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image_url
    return featured_image_url

def marsFacts():
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    tables = pd.DataFrame(tables[0])
    mars_table = tables.to_html(index=True,header=True)
    return mars_table

def marsHemisphere():
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov'

    for hemisphere in hemispheres:
    
        img_title = hemisphere.find('h3').text
        img_url = hemisphere.find('a',class_='itemLink product-item')['href']
        browser.visit(main_url + img_url)    
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        full_img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title":img_title,"img_url":full_img_url})

    return hemisphere_image_urls

