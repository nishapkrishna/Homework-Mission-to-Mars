# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
   
    exec_path = {'executable_path': 'C:/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest  title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary / MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Space Images through splinter module
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)
        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag
        new_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url and scrapped route
        new_image_url = main_url + new_image_url

        # Display full link to featured image
        new_image_url 

        # Dictionary / FEATURED IMAGE
        mars_info['new_image_url'] = new_image_url 
        
        return mars_info
    finally:

        browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all tweets
        weather_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Look for entries that display weather tweets
        for tweet in weather_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary / WEATHER TWEET
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column 
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder 
    data = mars_df.to_html()

    # Dictionary / MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image  
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append all the information into dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        return mars_info
    finally:

        browser.quit()