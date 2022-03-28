# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Create a function
def scrape_all():

    # Set up Splinter executable path and initialise headless Chrome browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Create function
def mars_news(browser):

    # ### Top News Articles and Summaries
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse the HTML
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    try:
        # Scrape the article title
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
        
    return news_title, news_paragraph    

# Create function
def featured_image(browser):

    # ### Featured Images
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'    
   
    return img_url

# Create function
def mars_facts():

    # Add try/except for error handling
    try:
        # ### Table of Facts
        # Scrape table in to pandas dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-dark table-bordered")

# Create function
def hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere. 
    # Loop through the full-resolution image URL, click the link, find the Sample image anchor tag, and get the href and title. 
    # Iterate through each of the four hemispheres images
    for i in range(4):
        # Find image and click link
        browser.links.find_by_partial_text('Hemisphere')[i].click()
        # Parse the html
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        
        # Add try/except for error handling
        try:
            # Retrieve url
            img_url = hemi_soup.find('li').a.get('href')
            # Retrieve title
            title = hemi_soup.find('h2', class_='title').get_text()
        
        except BaseException:
            return None

        # Create empty dictionary to store url and title
        hemispheres = {}
        # Use base url to create absolute url
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        # Add hemispheres dictionary to hemisphere_image_urls list
        hemisphere_image_urls.append(hemispheres)
        # Navigate back to the beginning to get next hemisphere image
        browser.back()
    return hemisphere_image_urls

# Define main behavior
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    