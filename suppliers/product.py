# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##@brief Doxygen style comments
##@package Katia.Product

from pathlib import Path
import pandas as pd
from loguru import logger

from strings_formatter import StringFormatter
formatter = StringFormatter()
from ini_files_dir import Ini
ini = Ini()
import execute_json as json

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
##'''
##ID
##Active (0/1)
##Name*
##Categories (x,y,z...)
##Price tax excluded
##Price tax included
##Tax rule ID
##Cost price
##On sale (0/1)
##Discount amount
##Discount percent
##Discount from (yyyy-mm-dd)
##Discount to (yyyy-mm-dd)
##Reference #
##Supplier reference #
##Supplier
##Brand
##EAN13
##UPC
##MPN
##Ecotax
##Width
##Height
##Depth
##Weight
##Delivery time of in-stock products:
##Delivery time of out-of-stock products with allowed orders:
##Quantity
##Minimal quantity
##Low stock level
##Send me an email when the quantity is under this level
##Visibility
##Additional shipping cost
##Unit for base price
##Base price
##Summary
##Description
##Tags (x,y,z...)
##Meta title
##Meta keywords
##Meta description
##Rewritten URL
##Label when in stock
##Label when backorder allowed
##Available for order (0 = No, 1 = Yes)
##Product availability date
##Product creation date
##Show price (0 = No, 1 = Yes)
##Image URLs (x,y,z...)
##Image alt texts (x,y,z...)
##Delete existing images (0 = No, 1 = Yes)
##Feature (Name:Value:Position:Customized)
##Available online only (0 = No, 1 = Yes)
##Condition
##Customizable (0 = No, 1 = Yes)
##Uploadable files (0 = No, 1 = Yes)
##Text fields (0 = No, 1 = Yes)
##Action when out of stock
##Virtual product (0 = No, 1 = Yes)
##File URL
##Number of allowed downloads
##Expiration date (yyyy-mm-dd)
##Number of days
##ID / Name of shop
##Advanced Stock Management
##Depends on stock
##Warehouse
##Accessories (x,y,z...)
##'''
# Copyright (c) 2020 e-cat.me  All rights reserved.
class Product():
  
    ##@param fields : pd.DataFrame 
    #поля товара 
    fields : pd.DataFrame = attrib(init = False, default = None)

    ##@param combinations : pd.DataFrame
    #поля комбинаций товара
    combinations : pd.DataFrame = attrib(init = False, default = None)
    

    ##@param attributes : pd.DataFrame
    #поля аттрибутов товара
    attributes : pd.DataFrame = attrib(init = False, default = None)
   

    NUMBER_PICTURES_TO_SAVE : int= attrib(init=False, default=1)
    
    ## инициализация класса
    #
    #словарь полей товара определена в файле <prestashop>_product_fields.json
    #словарь полей комбинаций товара определена в файле <prestashop>_product_combination.json
    def __attrs_post_init__(self , *args, **kwards):
        self.fields = json.loads(Path(ini.paths.ini_files_dir , f'''prestashop_product_fields.json'''))
        self.combinations =json.loads(Path(ini.paths.ini_files_dir , f'''prestashop_product_combinations_fields.json'''))
        
    
    @attrs
    class err:
        def __attrs_post_init__(self , *args, **kwards):
            pass

        #def handler(ex:Exception , locator , field):
        #    ## 
        #    #@params ex
        #    #@params field
        #    #@params locator


        #    #field = None
        #    logger.error(f''' 
        #    {ex}, 
        #    locator {locator} , 
        #    field {field} ''')
        #    return False


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


        def set_categories():
            categories :str = ','.join(_current_node['prestashop_categories'].keys())
            field['categories'] = categories + ',2'

      

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
        set_supplier()
        
        return self

    def prepare_images(self, supplier, raw_imgs)->str:
        _out:str = None

        def _parse_webelement(we):
            if str(type(we)).lower().find('selenium') > 0 :
                ''' найден вебэлемент . 
                 @TODO - узнать какой аттрибут вытащить
                 '''
                logger.debug(f'''  
                найден вебэлемент . 
                @TODO - узнать какой аттрибут вытащить
                {raw_imgs} 
                ''')
            return we

        if raw_imgs is None: 
            raw_imgs = ''
            _out = ''

        if isinstance(raw_imgs, str):
            _out = _parse_webelement(raw_imgs[0])
           
        elif isinstance(raw_imgs , list):
            if self.NUMBER_PICTURES_TO_SAVE == 1:
                _out = _parse_webelement(raw_imgs[0])
            else:
                for i in raw_imgs:
                  _out += _parse_webelement(i)
        return _out               
            

        
        logger.debug(f''' 
        ссылки на картинки 
        {imgs}
        ''')
