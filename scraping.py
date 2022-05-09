
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #automated browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    #Set news title and article variable
    news_title, news_paragraph = mars_news(browser)

    #Store data results
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop driver and return data
    browser.quit()
    return data



# Scraping latest article function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Parse through html data and store article 
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        #Set parent tag parsed data to variable
        slide_elem = news_soup.select_one('div.list_text')

        #Find title from article
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browswer):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ### Mars Facts
def mars_facts():
    #Add try/except error handling
    try:
        #read html data as datafram
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #assign columns and set index    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #Extport df to html
    return df.to_html()

## Function Call with Flask
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

