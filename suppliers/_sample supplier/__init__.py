# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module
from typing import List
import execute_json as json
from pathlib import Path
import pandas as pd
from attr import attrib, attrs, Factory
from selenium.webdriver.remote.webelement import WebElement 
from selenium.webdriver.common.keys import Keys
from strings_formatter import StringFormatter
from products import Product


formatter = StringFormatter()
stores : list = []
''' ------------------ НАЧАЛО -------------------------- '''

def login(s) -> bool :

    _ =  s.locators['login']
    _d = s.driver
    try:
        _d.get('')
        #_d.switch_to_frame(0) 
        _d.find(_['user_locator']).send_keys(_['user'])
        _d.find(_['password_locator']).send_keys(_['password'])
        _d.find(_['send_locator']).click()
        return True

    #try:
    #    ''' всякие банннеры '''
    #    s.driver.find(locators['close banner'])[0].click()
    #    s.driver.find(locators['open_login_popup_button'])[0].click()
    #    s.driver.find(locators['open_login_popup_button']['open_login_popup_button 2lvl'])[0].click()

    #except Exception as ex: return False, print(ex)


    #try:
    #    s.driver.find(locators['user_locator'])[0].send_keys( locators['user'])
    #    s.driver.find(locators['password_locator'])[0].send_keys( locators['password'])
    #    s.driver.find(locators['send_locator'])[0].click()

    except Exception as ex:return False, print(ex)
    ''' ------------------ КОНЕЦ -------------------------- '''

    ''' ------------------ НАЧАЛО -------------------------- '''

def set_start_settings(s)->bool:
    _ =  s.locators['currency_laguage_country_locators']
    _d = s.driver
    _d.find(_['country_locator']).send_keys('Israel')
    _d.find(_['currency_locator']).send_keys(Keys.RETURN)

''' ------------------ НАЧАЛО -------------------------- '''
stores:list = []
def run_stores(s):
    '''  
    Запускает сценарий сбора товаров по определенным в сценарии магазинам поставщика 
    -------------------------
    s : текущий Supplier
    '''
    stores_groups_files_dict = json.loads(Path(s.SCENARIES_DIRECTORY , f'''{s.}.json'''))['scenaries']
    for stores_group_file in stores_groups_files_dict:
        stores_dict = json.loads(Path(s.SCENARIES_DIRECTORY , f'''{stores_group_file}'''))
        try:
            for store_settings_dict in stores_dict.items(): 
                stores.append({
                'store ID': store_settings_dict[1]['store_id'] ,
                'pail': 1,
                'store description': store_settings_dict[1]['description'],
                'parent category': 3,
                'root': 0 ,
                'aliexpress_url' : store_settings_dict[1]['url'],
                'store_categories_json': store_settings_dict[1]['store_categories_json_file']
                })


                run_local_scenario(s,stores[-1])
                '''запускаю последний добавленный в список '''

        except Exception as ex:return False, print(ex)
    pass 
    ''' ------------------ КОНЕЦ  -------------------------- '''


''' ------------------ НАЧАЛО -------------------------- ''' 
def get_json_from_store(s , store_settings_dict : dict = {}) -> dict:
    ''' у каждого магазина в алиэкспресс можно запросить файл 
    https://aliexpress.com/store/store/productGroupsAjax.htm?storeId=<storeId>&shopVersion=3.0&callback=<callback>
    в нем заложена структура внутренних категорий магазина
    по нему можно проверять изменения в структуре магазина
    '''


    s.driver.get_url(store_settings_dict['store_categories_json'] )
    json_from_store = s.driver.find(s.locators['store']['data_from_store_json_file'])[0].text
    return json_from_store


''' ------------------ НАЧАЛО -------------------------- ''' 
def build_shop_categories(s , store_settings_dict : dict) -> dict:   

   
    s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
    #try:
    #    s.driver.find(s.locators['eng version'])[0].click()
    #except Exception as ex : print(ex)
    
    if s.driver.current_url != store_settings_dict[1]['all-wholesale-products']:
        if str(s.driver.current_url).find('login.aliexpress')>0:login(s)
        else:print(s.driver.current_url)
        s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
        pass


    categoties_blocks_html = s.driver.find(s.locators['store']['sub_block_main_item'])[0]
    elements = categoties_blocks_html.find_elements_by_xpath("//*[@class='group-item']")
    
    for  el in elements:
        main_category = el.find_elements_by_tag_name("a")[0]
        main_category_name = main_category.get_attribute('text')
        main_category_url = main_category.get_attribute('href')
        main_category_url_list = main_category_url.split('/')[-1].split('.')[0].split('_')
        main_category_id = main_category_url_list[-1]
        shop_id = main_category_url_list[0]
        t.append({
                'category ID': main_category_id ,
                'pail': 1,
                'category name': main_category_name,
                'parent category': shop_id,
                'root': 0 ,
                'aliexpress_url' : main_category_url
                })

        sub_blocks = el.find_elements_by_tag_name("ul")
        if len(sub_blocks)>0: 
            subs = sub_blocks[0].find_elements_by_tag_name("a")
            for sub in subs:
                sub_category_name = sub.get_attribute('text')
                sub_category_url = sub.get_attribute('href')
                sub_category_url_list = sub_category_url.split('/')[-1].split('.')[0].split('_')
                sub_category_id = sub_category_url_list[-1]
                shop_id = sub_category_url_list[0]
                t.append({
                    'category ID': sub_category_id ,
                    'pail': 1,
                    'category name': sub_category_name,
                    'parent category': main_category_id,
                    'root': 0 ,
                    'aliexpress_url' : sub_category_url
                    })
                
    
    s.export(data = t , format = ['csv'] )
    pass
    ''' ------------------ КОНЕЦ  -------------------------- '''

def run_local_scenario(s, store_settings_dict: dict = {}):
    json_from_store = get_json_from_store(s, store_settings_dict)
    #s.export(ajax_from_store , ['json'] , store_settings_dict['store ID'])
    #print(f''' {store_settings_dict['store ID']} added''')
    pass



    ''' ------------------ НАЧАЛО -------------------------- '''
products: list = []
def grab_product_page(s):
    _d = s.driver
    _d.scroll(3)
    _ : dict = s.locators['product']

    p : Product = Product(s=s)

    field = p.fields

    def get_id():
        field['id'] = _d.current_url.split('/')[-1].split('.')[0]
        ''' выдергиваю из 
        https://www.aliexpress.com/item/00000000000000.html? 
        '''
       
    def get_title():
        field['title'] = _d.find(_['product_title_locator'])[0]
    def get_price():
        _price = _d.find(_['product_price_locator'])[0]
        field['price'] = formatter.clear_price(_price)
    def get_shipping():
        _shipping = _d.find(_['product_delivery_locator'])
        for s in _shipping:
            field['shipping price'] = formatter.clear_price(s)
    def get_images():
        _images = _d.find(_['product_images_locator'])
        for k,v in _images.items():
               field['img url'] += f''' {v}, '''
               field['img alt'] += f''' {k}, '''
    def get_attributes():
        _attributes = _d.find(_['product_attributes_locator'])
        return _attributes
    def get_qty():
        _qty = _d.find(_['product_qty_locator'])
        _qty = formatter.clear_price(_qty)
        return _qty
    def get_byer_protection():
        _byer_protection = _d.find(_['product_byer_protection_locator'])
        return _byer_protection
    def get_description():
        _description = _d.find(_['product_description_locator'])
        return _description
    def get_specification():
        specification = _d.find(_['product_specification_locator'])
        return specification
    def get_customer_reviews():
        _customer_reviews = _d.find(_['product_customer_reviews_locator'])
        return _customer_reviews



    get_id(),
    get_title(),
    get_price(),
    get_shipping(),
    get_images(),
    get_attributes(),
    get_qty(),
    get_byer_protection(),
    get_description(),
    get_specification(),
    get_customer_reviews()
        

    pass





