# -*- coding: utf-8 -*-
#!/usr/bin/env python
#@package katia.suppliers.aliexpress

#Documentation for this module
from typing import List
from pathlib import Path
import pandas as pd
import pickle
from script_logger import logger
from attr import attrib, attrs, Factory

import execute_json as json
from selenium.webdriver.remote.webelement import WebElement 
from selenium.webdriver.common.keys import Keys
from strings_formatter import StringFormatter as SF
from suppliers.product import Product


#formatter = StringFormatter()
stores : list = []

## paginator
def pagination(s):
    _d = s.driver
    _ = s.locators
    _d.scroll(7)
    list_product_urls : list = _d.find(_['product']['link_to_product_locator'])
    pagination_block = _d.find(_['pagination_block_locator'])
    ## Одна страница категории
    if pagination_block is None:
        return list_product_urls
    ## Много страниц в категории
    for item in pagination_block:
        for k,v in item.items():
            if str(k).find('Next') < 0:
                _d.get_url(v)
                list_product_urls += _d.find(_['product']['link_to_product_locator'])
    return list_product_urls
        
## login etc.
def login(s) -> bool :
    def _login() -> bool:
        _ =  s.locators['login']
        _d = s.driver

        _d.get(_['login_url'])
        _d.get('https://www.aliexpress.com')

        _d.dump_cookies_to_file()

    def _set_language_currency_shipto() -> bool:
        _ =  s.locators['currency_language_shipto_locators']
        _d = s.driver

        '''@todo
            сделать механизм 
            сохранения загрузки файлов печенек
        '''
        _d.load_cookies_from_file(_d.cookies_file_path)
        _d.get_url('https://www.aliexpress.com')
        

        if _d.click(_['block_opener_locator']):_d.wait(1)
        if _d.click(_['shipto_locator']):_d.wait(.7)
        if _d.click(_['language_locator']):_d.wait(.7)
        if _d.click(_['currency_locator']):_d.wait(.7)
        if _d.click(_['save_button_locator']):_d.wait(.7)

        _d.dump_cookies_to_file()

    #_login()
    _set_language_currency_shipto() 
    



stores:list = []
def run_stores(s):
    
    stores_groups_files_dict = json.loads(Path(s.SCENARIES_DIRECTORY , f'''aliexpress.json'''))['scenaries']
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

        except Exception as ex:return False, logger.error(ex)
    pass 
    ''' ------------------ КОНЕЦ  -------------------------- '''

## try to get json fro file
def get_json_from_store(s , store_settings_dict : dict = {}) -> dict:
    ''' у каждого магазина в алиэкспресс можно запросить файл 
    https://aliexpress.com/store/store/productGroupsAjax.htm?storeId=<storeId>&shopVersion=3.0&callback=<callback>
    в нем заложена структура внутренних категорий магазина
    по нему можно проверять изменения в структуре магазина
    '''


    s.driver.get_url(store_settings_dict['store_categories_json'] )
    json_from_store = s.driver.find(s.locators['store']['data_from_store_json_file'])[0].text
    return json_from_store

## build_shop_categories
def build_shop_categories(s , store_settings_dict : dict) -> dict:   

   
    s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
    #try:
    #    s.driver.find(s.locators['eng version'])[0].click()
    #except Exception as ex : logger.error(ex)
    
    if s.driver.current_url != store_settings_dict[1]['all-wholesale-products']:
        if str(s.driver.current_url).find('login.aliexpress')>0:login(s)
        else:logger.error(s.driver.current_url)
        s.driver.get_url(store_settings_dict[1]['all-wholesale-products'])
        pass


    categoties_blocks_html = s.driver.find(s.locators['store']['sub_block_main_item'])[0]
    elements = categoties_blocks_html.find_elements_by_xpath("//*[@class='group-item']")
    
    for  el in elements:
        main_category = el.find_elements_by_tag_name("a")[0]
        main_category_name = main_category.set_attribute('text')
        main_category_url = main_category.set_attribute('href')
        main_category_url_list = main_category_url.split('/')[-1].split('.')[0].split('_')
        main_category_id = main_category_url_list[-1]
        shop_id = main_category_url_list[0]
        el.append({
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
                sub_category_name = sub.set_attribute('text')
                sub_category_url = sub.set_attribute('href')
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

## run_local_scenario
def run_local_scenario(s, store_settings_dict: dict = {}):
    json_from_store = get_json_from_store(s, store_settings_dict)
    #s.export(ajax_from_store , ['json'] , store_settings_dict['store ID'])
    #logger.error(f''' {store_settings_dict['store ID']} added''')
    pass



    ''' ------------------ НАЧАЛО -------------------------- '''

products: list = []
## grab_product_page
def grab_product_page(s , p):
    p.grab_product_page(s)



    _ : dict = s.locators['product']
    _d = s.driver
    _d.scroll(3)
    _field = p.fields
    _combinot = p.combinations
    

    

    def set_id():
        _field['id'] = _d.current_url.split('/')[-1].split('.')[0]
    def set_sku_suppl():
        _field['mkt_suppl'] = _field['id']


    ##
    def set_supplier():pass
    '''  '''
            


    ## set_title
    def set_title():
        try: 
            _field['title'] = _d.find(_['product_title_locator'])
            _field['title'] = SF.remove_special_characters(_field['title'])
        except Exception as ex: print (f''' Exception   {ex} in set_title() ''')
            
    ## set_price
    def set_cost_price():
        _price = _d.find(_['product_price_locator'])
        try:
            _price = SF.clear_price(_price)
            _field['cost price'] = _price
            return True
        except Exception as ex: print (f''' Exception   {ex} in set_cost_price() ''')


    ## set_delivery    
    def set_delivery():pass
        #_shipping = _d.find(_['product_shipping'])
        #for s in _shipping:
        #    field['shipping price'] = formatter.clear_price(s)


    ## set_images
    def set_images():
        imgs : str = ''
        
        _i = _d.find(_['product_main_image_locator'])
        
        _i = _i.replace('.webp','')
        ''' если расширение файла .webp 
        то я его убираю в надежде, что за ним прячется 
        настоящий формат'''

        if _i[:-1]=='_':
            ''' вполне попадается _ после .jpg 
            имеет вид .jpg_'''
            _i = _i[1:-1]
        _field['img url'] = _i


        _images_thumb_50x50 : str = None
        def replace_suffics():
            for i in _images_thumb_50x50:
                imgs += f''' {str(i).replace('_50x50.jpg','')},'''
            _field['img url'] = imgs
   





    ## set_combinations
    def set_combinations():
        _combina = json.loads(Path(s.SCENARIES_DIRECTORY , f'''prestashop_product_combinations_fields.json'''))
        _attr_position = 0

        def set_values():

            _combina['Product ID'] = _field['id']

            _price = _d.find(_['product_price_locator'])
            _price = SF.clear_price(_price)

            _qty = _d.find(_['product_qty_locator'])[0]
            _qty = SF.clear_price(_qty)



            ## форма комбинаций  в Prestashop
            # Attribute (Name:Type:Position)*
            # Value (Value:Position)*

            attr_name = _d.find(_title)
            attr_type = 'select'
            attr_position = _attr_position

            _combina['Attribute (Name:Type:Position)'] = f'''{attr_name}:{attr_type}:{attr_position}'''
        
            _vt = _d.find(_['product_combinations_container_locator']['product_combinations_value_title'])
            _vp = _attr_position
            _combina['Value (Value:Position)'] = f'''{_vt}:{_vp}'''

                

            url_dict = _d.get_dict_from_urlstr()
            _combina['Supplier reference'] = _combina['Product reference'] = url_dict['params']['sku_id']
                
                
            _d.find(_['product_title_locator'])

            _combina['Image URLs(x,y,z)'] = _d.find(_['product_main_image_locator'])
            _combina['Quantity'] = _qty
            _combina['Wholesale price'] = _price

        try:
            
            _title = _['product_combinations_container_locator']['product_combinations_title']
            _values_locator = _['product_combinations_container_locator']['image_attribute_locator'] 
            _values = _d.find(_values_locator)
            if _values == None: return False
            ''' нет комбинаций '''
            
            if isinstance(_values , list):
                ''' несколько вариантов товара'''
                for x in _values:
                    ''' нажимаю на каждую опцию товара '''
                    x.click()
                    set_values()
                    _combinot.apply(_combina)

            else:
                ''' один вариант '''
                _values.click()
                set_values()
                _combinot.apply(_combina)
                



                
            return True
        except Exception as ex: 
            
            logger.error(ex)
            return False


    ## set_qty
    def set_qty():
        try:
            _qty = _d.find(_['product_qty_locator'])[0]
            _field['qty'] = SF.clear_price(_qty)
            return True
        except Exception as ex: 
            #field['qty'] = None
            logger.error(ex)
            return False

    def set_byer_protection():
        try:
            _field['product_byer_protection'] = _d.find(_['product_byer_protection_locator'])
            return True
        except Exception as ex: 
            _field['product_byer_protection'] = None
            logger.error(ex)
    def set_description():
        try:
            _field['product_description'] = _d.find(_['product_description_locator'])
            return True
        except Exception as ex: 
            _field['product_description'] = None
            logger.error(ex)

    def set_specification():
        try:
            _field['product_specification'] = _d.find(_['product_specification_locator'])
            return True
        except Exception as ex: 
            _field['product_specification'] = None
            logger.error(ex)
    def set_customer_reviews():
        try:
            _field['product_customer_reviews'] = _d.find(_['product_customer_reviews_locator'])
        except Exception as ex:
            _field['product_customer_reviews'] = None
            logger.error(ex)


    set_id()
    set_sku_suppl()
    set_title()
    set_cost_price()
    set_delivery()
    set_images()
    set_combinations()
    set_qty()
    set_byer_protection()
    set_description()
    set_specification()
    set_customer_reviews()
        

    return p



def list_product_urls_from_pagination(supplier):
    ''' листалка '''
    _s = supplier
    _d = _s.d
    _l = _s.locators['product']['link_to_product_locator']

    list_product_urls : list = _d.find(_l)
    pages = _d.find(_s.locators['pagination']['a'])
    if isinstance(pages,list):
        for page in pages:
            list_product_urls.append(_d.find(_l))
            _perv_url = _d.current_url
            page.click()
            if _perv_url == _d.current_url:break
    return list_product_urls









