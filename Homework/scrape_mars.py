from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd


def init_browser(): 
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
	browser = init_browser()
	def info(url):
		browser.visit(url)
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
		return soup
	
	mars_data={}


	nasa_news_soup = info('https://mars.nasa.gov/news/')
	list_of_news = nasa_news_soup.find_all('li',class_='slide')
	news_title = list_of_news[0].find('div',class_='content_title').text
	news_title


	news_p = list_of_news[0].find('div',class_='article_teaser_body').text


	news_date = list_of_news[0].find('div',class_='list_date').text


	mars_data['News Title'] = news_title
	mars_data['News Paragraph'] = news_p
	mars_data['News Date'] = news_date



	base_url = 'https://www.jpl.nasa.gov'
	url_image = base_url+ '/spaceimages/?search=&category=Mars'

	image_soup = info(url_image)


	all_img = image_soup.find_all('a',class_= 'button fancybox')[0]
	

	featured_img_link = base_url + all_img['data-link']

	large_img_soup = info(featured_img_link)


	featured_image_url= base_url +  large_img_soup.find('article').find('figure',class_='lede').find('a')['href']
	


	mars_data['Featured Image Url'] = featured_image_url

	tweeter_url='https://twitter.com/marswxreport?lang=en'


	tweeter_soup = info(tweeter_url)

	mars_weather = tweeter_soup.find('div',class_='content').find('div',class_="js-tweet-text-container").find('p').text


	mars_data['Latest Weather on Mars'] = mars_weather


	facts_url = 'https://space-facts.com/mars/'


	facts_tables = pd.read_html(facts_url)



	facts_df = facts_tables[0]


	facts_df.columns = ['properties', 'data']
	


	facts_html_table = facts_df.to_html(index=False).replace('\n', '')


	mars_data['Mars Facts'] = facts_html_table


	hemisphere_base_url = 'https://astrogeology.usgs.gov'
	hemisphere_url = hemisphere_base_url+'/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	hemisphere_soup = info(hemisphere_url)



	hemisphere_list = hemisphere_soup.find_all('div',class_='item')


	hemisphere_image_urls=[]
	for element in hemisphere_list:
		hemisphere_dict = {}
		link = hemisphere_base_url + element.find('a')['href']
		title = element.find('h3').text
		hemisphere_dict['title'] = title
		
		soup = info(link)
		img_link = soup.find_all('a',target='_blank')[0]['href']
		hemisphere_dict['img_url'] = img_link
		
		hemisphere_image_urls.append(hemisphere_dict)
		time.sleep(3)


	mars_data['Mars Hemisphere'] = hemisphere_image_urls
	
	return mars_data





