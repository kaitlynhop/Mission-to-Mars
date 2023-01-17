
# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import datetime as dt

# main function to instantiate driver
def scrape_all():
    
    # Set up Splinter web browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # store mars news return variable and call funciton
    news_title, news_p = mars_news(browser)
    # store all data 
    data = {
        "news_title": news_title, "news_p": news_p, 
        "img_url": featured_image(browser), 
        "facts": mars_facts(), "hemispheres": mars_imgs(browser),
        "last_modified": dt.datetime.now()}

    # quit automated browser
    browser.quit()
    # return data
    return data


## MARS SCRAPE
# news scrape function
def mars_news(browser):
    # news url
    url = 'https://redplanetscience.com/'
    # set browser to visit url
    browser.visit(url)
    # search for uniqe tags and delay for page loading with browser
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # set up soup instance
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # use try/except to search tags that were found at the time of inspection
    try:
        # select the first article by tag and class
        slide_elem = news_soup.select_one('div.list_text')
        # store title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # get article body
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


# ### Image Data
def featured_image(browser):
# image url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # use web-driver to click full image button - using text
    full_img_btn = browser.links.find_by_partial_text('FULL IMAGE')
    full_img_btn.click()

    ## set up parser
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # scrape image data
        mars_img = img_soup.find('img', class_='fancybox-image').get('src')
        # create full url for image
        img_url = f'https://spaceimages-mars.com/{mars_img}'
    except AttributeError:
        return None

    return img_url

# ### Mars Facts - Table Data
def mars_facts():
    try:
        # read first table directly into df
        df = pd.read_html("https://galaxyfacts-mars.com/")[0]

        # set the column names
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
    except BaseException:
        return None

# convert df back to html to use on site
    return df.to_html()

def mars_imgs(browser):
    # url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # store list
    img_urls = []
    #parse first page
    html = browser.html
    mars_soup = soup(html, "html.parser")
    # loop through first page
    try:
        mars_imgs = mars_soup.find_all('div', class_='description')

        for img in mars_imgs:
            img_title = img.a.h3.text
            img_link = browser.links.find_by_partial_text(img_title).click()
            html_img = browser.html
            mars_soup = soup(html_img, 'html.parser')
            jpg_url = mars_soup.select_one('a[href$=".jpg"]').get('href')
            mars_img_data = {'img_url': url + jpg_url, 
                            'img_title': img_title}
            img_urls.append(mars_img_data)
            browser.back()

    except BaseException:
        return None

    return img_urls

# how to run file
# if __name__ == "__main__":
    # fx call to print
    # print(scrape_all())
