# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##@brief Doxygen style comments
##@package Katia.Product
import inspect
import pandas as pd
from pathlib import Path
import GLOBAL_SETTINGS
import execute_json as json
logger = GLOBAL_SETTINGS.logger
formatter = GLOBAL_SETTINGS.SF
NUM_OF_IMAGES_TO_BE_SAVED = GLOBAL_SETTINGS.NUM_OF_IMAGES_TO_BE_SAVED
SCENARIES_DIRECTORY = GLOBAL_SETTINGS.SCENARIES_DIRECTORY
CATEGORIES_EXCLUDED_FROM_METAWORDS = GLOBAL_SETTINGS.CATEGORIES_EXCLUDED_FROM_METAWORDS

#from ini_files_dir import Ini

#ini = Ini()
#import execute_json as json

from attr import attrs, attrib, Factory
@attrs
##Product()
# @file product.py
#
# @brief Определение класса Product().
#
# @section description_product Description
# Defines the base and end user classes for various sensors.
# - Sensor (base class)
# - TempSensor
#
# @section libraries_product Libraries/Modules
# - random standard library (https://docs.python.org/3/library/random.html)
#   - Access to randint function.
#
# @section notes_product Notes
# - Comments are Doxygen compatible.
#
# @section todo_product TODO
# - None.
#
# @section author_product Author(s)
# - Created by Katia on 19/06/2022.
#

## ID
## Active (0/1)
## Name*
## Categories (x,y,z...)
## Price tax excluded
## Price tax included
## Tax rule ID
## Cost price
## On sale (0/1)
## Discount amount
## Discount percent
## Discount from (yyyy-mm-dd)
## Discount to (yyyy-mm-dd)
## Reference #
## Supplier reference #
## Supplier
## Brand
## EAN13
## UPC
## MPN
## Ecotax
## Width
## Height
## Depth
## Weight
## Delivery time of in-stock products:
## Delivery time of out-of-stock products with allowed orders:
## Quantity
## Minimal quantity
## Low stock level
## Send me an email when the quantity is under this level
## Visibility
## Additional shipping cost
## Unit for base price
## Base price
## Summary
## Description
## Tags (x,y,z...)
## Meta title
## Meta keywords
## Meta description
## Rewritten URL
## Label when in stock
## Label when backorder allowed
## Available for order (0 = No, 1 = Yes)
## Product availability date
## Product creation date
## Show price (0 = No, 1 = Yes)
## Image URLs (x,y,z...)
## Image alt texts (x,y,z...)
## Delete existing images (0 = No, 1 = Yes)
## Feature (Name:Value:Position:Customized)
## Available online only (0 = No, 1 = Yes)
## Condition
## Customizable (0 = No, 1 = Yes)
## Uploadable files (0 = No, 1 = Yes)
## Text fields (0 = No, 1 = Yes)
## Action when out of stock
## Virtual product (0 = No, 1 = Yes)
## File URL
## Number of allowed downloads
## Expiration date (yyyy-mm-dd)
## Number of days
## ID / Name of shop
## Advanced Stock Management
## Depends on stock
## Warehouse
## Accessories (x,y,z...)


class Product():
  
    supplier = attrib(kw_only = True, default = None)  

    ##@param fields : pd.DataFrame 
    #поля товара 
    fields : list = attrib(init = False, default = None)

    ##@param combinations : pd.DataFrame
    #поля комбинаций товара
    combinations : pd.DataFrame = attrib(init = False, default = None)
    

    ##@param attributes : pd.DataFrame
    #поля аттрибутов товара
    attributes : pd.DataFrame = attrib(init = False, default = None)
   

    ## инициализация класса
    #
    #словарь полей товара определена в файле <prestashop>_product_fields.json
    #словарь полей комбинаций товара определена в файле <prestashop>_product_combination.json
    def __attrs_post_init__(self , *args, **kwards):

        self.fields = json.loads(Path(GLOBAL_SETTINGS.INI_DIRECTORY , f'''prestashop_product_fields.json'''))
        self.combinations = json.loads(Path(GLOBAL_SETTINGS.INI_DIRECTORY , f'''prestashop_product_combinations_fields.json'''))
        self.grab_product_page(self.supplier)

    ##собраю локаторами нужные мне позиции со страницы товара 
    #collect the positions from the product page with locators
    def grab_product_page(self , s):
      
        _d = s.driver
        _ : dict = s.locators['product']
        _current_node = s.current_node
        field = self.fields
            
        def set_id():pass
        def set_sku_suppl():pass
        def set_supplier(): pass
        def set_title():pass
        def set_cost_price():pass
        def set_before_tax_price():pass
        def set_delivery():pass
        def set_images():pass            
        def set_combinations():pass
        def set_qty():pass
        def set_byer_protection():pass
        def set_description():pass
        def set_specification():pass
        def set_customer_reviews():pass

        def set_meta_title():
            _meta_title :str = list(_current_node['prestashop_categories'].values())[0]
            field['meta title'] = _meta_title

        def set_meta_keywords():
            _keywords = ''
            '''
            У меня есть два словаря:
            один из сценария,
            второй - словарь исключений

            Ключи словаря - это множество. Множества можно вычитать:

                a = {'title': 'jr', 'description': '64', 'price': '3'}
                b = {'python': 'dede', 'key:': '#789', 'title': 'jr', 'description': '64', 'price': '3'}
                print(a.keys()-b.keys())
                print(b.keys()-a.keys())

                https://ru.stackoverflow.com/questions/1328408/%D0%9A%D0%B0%D0%BA-%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B8%D1%82%D1%8C-%D0%B4%D0%B2%D0%B0-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8F-python-%D0%B8-%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C-%D0%BA%D0%B0%D0%BA%D0%B8%D1%85-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9-%D0%BD%D0%B5%D1%82-%D0%B2-%D1%82%D0%BE%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%B8%D0%BD%D0%BE%D0%BC-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B5
            '''
            _keywords_keys = list(_current_node['prestashop_categories'].keys() - CATEGORIES_EXCLUDED_FROM_METAWORDS.keys())

            for k in _keywords_keys:
                keyword = _current_node['prestashop_categories'].get(k)
                if _keywords == '': _keywords = keyword
                _keywords = f'''{_keywords},{keyword}'''
            field['meta keywords'] = _keywords

        def set_categories():
            _categories :str = ','.join(_current_node['prestashop_categories'].keys())
            field['categories'] = _categories + ',2'

      

        set_id()
        set_sku_suppl()
        set_title()
        set_supplier()
        set_cost_price()
        set_before_tax_price()
        set_delivery()
        set_images()
        set_combinations()
        set_qty()
        set_byer_protection()
        set_description()
        set_specification()
        set_customer_reviews()
        set_categories()
        set_meta_title()
        set_meta_keywords()
        set_supplier()
        
        return self

    def get_certain_amount_of_images(self, supplier, raw_imgs)->str:
        _out:str = ''


        if raw_imgs is None: pass 
  
        elif isinstance(raw_imgs, str):
            _out = raw_imgs
           
        elif isinstance(raw_imgs , list):
            _counter = 0
            for i in raw_imgs:
                _out = _out + i
                _counter += 1
                if _counter >= NUM_OF_IMAGES_TO_BE_SAVED: break
        return _out               
         