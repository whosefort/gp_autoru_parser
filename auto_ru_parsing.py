import logging
import pandas as pd
import numpy as np
import bs4
import requests
import re
import time
from selenium import webdriver
from random import randint

class AutoRuParser:
    def __init__(self):
        # https://stackoverflow.com/questions/61114980/can-selenium-automation-be-used-with-bs4
        #https: // docs.python.org / 3 / library / logging.html
        self.logger = logging.getLogger(__name__)
        self.driver = webdriver.Chrome()
        self.main_page_url = "https://www.auto.ru/moskva/cars/all/?page="

    def parse_car_html(self, card):
        card_name_el  = card.find('a', class_=re.compile("ListingItemTitle__link"))
        name, price, year, mileage, specs, city, seller, link  = ("_")*8
        if card_name_el: name = card_name_el.get_text()
        else: name = "_"

        if card_name_el and card_name_el.has_attr("href"): link = card_name_el["href"]
        else: link = "_"

        if name=="_": return None

        price_block = card.find('div', class_=re.compile(r'ListingItemUniversalPrice__title'))
        if price_block: price_el = price_block.find('div')
        else: price_el = "_"
        if price_el!="_":
            price_string = price_el.get_text()
            price_digits = "".join(re.findall(r'\d+', price_string))
            if len(price_digits)>0:
                price = int(price_digits)
            else:
                price = "_"
        spec_blocks = card.find_all('div', class_=re.compile(r'ListingItemUniversalSpecs__spec-'))
        specs = []
        for block in spec_blocks:
            specs.append(block.get_text().replace('\xa0', ' '))
        year_mileage_block = card.find('div', class_=re.compile(r'ListingItemUniversalCondition'))
        if year_mileage_block:
            year_el = year_mileage_block.find('div', class_=re.compile(r'Typography2__h5'))
        else:
            year_el = "_"
        if year_el!="_":
            year_string = year_el.get_text()
        else:
            year_string = "_"
        year_digits = "".join(re.findall(r'\d+', year_string))
        if len(year_digits)>0:
            year = int(year_digits)

        status_block = card.find('div', class_=re.compile(r'ListingItemUniversalCondition__status'))
        if status_block:
            mileage_el = status_block.find('div')
        else:
            mileage_el = "_"
        if mileage_el!="_":
            mileage_string = mileage_el.get_text()
        else:
            mileage_string = "_"
        mileage_digits = "".join(re.findall(r'\d+', mileage_string))
        if len(mileage_digits)>0:
            mileage = int(mileage_digits)
        else:
            mileage = "_"

        seller_block = card.find('div', class_=re.compile(r'ListingItemUniversalSeller__sellerName'))
        if seller_block:
            seller = seller_block.get_text()

        city_block = card.find('span', class_=re.compile(r'MetroListPlace__regionName'))
        if city_block:
            city = city_block.get_text()

        return {
            "name": name,
            "price": price,
            "year": year,
            "mileage": mileage,
            "specs": specs,
            "city": city,
            "seller": seller,
            "link": link
        }


    def get_page(self, page_num=0, first_time=True, parsed_page=None):
        if parsed_page==None:
            self.driver.get(self.main_page_url+str(page_num))
            if first_time:
                time.sleep(15)
            else:
                time.sleep(3)
            page = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        if parsed_page:
            page = bs4.BeautifulSoup(parsed_page, "html.parser")
        cards = page.find_all("div", class_=re.compile("ListingItemUniversal-"))
        res = []
        for card in cards:
            res.append(self.parse_car_html(card))
        return res

    def save_backup(self, data, f):
        list_to_pandas  = []
        for i  in data:
            for j in i:
                list_to_pandas.append(j)
        df = pd.DataFrame(list_to_pandas)
        df.drop_duplicates(["link"], inplace=True)
        df.to_csv(f, index=False, encoding="utf-8")

    def parse_to_dataframe(self, start_page, end_page, scrolls=500):
        final_list = []
        final_list.append(self.get_page(start_page, True))
        is_last_page = False
        try:
            for i in range(start_page+1, end_page+1):
                page = self.get_page(i, False)
                if page:
                    final_list.append(page)
                    self.logger.info(f"Page {i} of {end_page} successfully parsed")
                else:
                    self.logger.warning(f"Page {i} of {end_page} not parsed")
                    continue
                if i==99:
                    is_last_page = True
                    break
            while is_last_page and scrolls > 0:
                self.logger.info(f"Infinite scrolling started on last page: {scrolls}")
                #To perform smooth scroll that is not detected: https://developer.mozilla.org/en-US/docs/Web/API/Window/scrollBy
                #https: // www.geeksforgeeks.org / software - testing / selenium - scrolling - a - web - page /
                #https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python#27760083
                #mess around with website protection to get all elements from last page with infinite scrolling
                time.sleep(randint(5,30)/10)
                self.driver.execute_script("window.scrollBy({top:"+str(randint(400,900))+",left:0, behaviour:'smooth'})")
                chance = randint(0,100)
                time.sleep(randint(4,15)/10)
                if chance>50:
                    self.driver.execute_script("window.scrollBy({top:"+str(randint(-100,-50))+",left:0, behaviour:'smooth'})")
                if scrolls%11==0:
                    page = self.get_page(parsed_page=self.driver.page_source)
                    final_list.append(page)

                scrolls -= 1
        except Exception as e:
            self.logger.error(f"Critical error while parsing: {e}")
        finally:
            self.logger.info(f"Parser have finished with the number of parsed pages: f{len(final_list)}")
            self.save_backup(final_list,"cars_data.csv")




if __name__ == "__main__":
    a = AutoRuParser()
    a.parse_to_dataframe(start_page=0,end_page=98)


