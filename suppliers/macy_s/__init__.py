# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'e-cat.me'
##@package Katia
#Documentation for this module
#           Функции, присущие поставщику  KSP, которыми я дополняю класс supplier

from logger import Log

from bs4 import BeautifulSoup
import execute_json as json
from strings_formatter import StringFormatter
formatter = StringFormatter()
from suppliers.product import Product 

def product_attributes(self, p, delimeter, elements):
    i=0
    skip = False
    c = p.combinations 
    ''' просто сокращенная запись '''
    for e in build_list_from_html_elements(self, delimeter, elements):
        if i%2 == 0:

            if not p.skip_row(e):
                '''
                -----^^^^^^^^^^   
                слова в колонке, которые надо пропустить находятся в файле
                prestashop_product_combinations_sysnonyms_<lg>.json['skip']
                '''
                i+=1
                skip = True
                continue

            attr = formatter.remove_HTML_tags(e)
            ''' первое значение '''
            if c["Attribute (Name:Type: Position)"] == "": c["Attribute (Name:Type: Position)"] = f'''{attr}:select:0'''
            else: c["Attribute (Name:Type: Position)"] += f''', {attr}:select:0'''
            ''' остальные значения '''
        else:
            if skip:
                i+=1        
                skip = False
                continue

            val = e.next
            if c["value (Name:Type: Position)"] == "":c["value (Name:Type: Position)"] = f'''{e.next}:select:0'''
            else: c["value (Name:Type: Position)"] += f''',{e.next}:select:0'''
        i+=1
        pass


def grab_product_page(s) -> Product:
    _d = s.driver
    _ : dict = s.locators['product']

    p : Product = Product(s=s).grab_product_page()
    ''' 
    Вытаскиваю со страницы товара все поля по локаторам
    ------------
    p - товар
    '''
    
    #field = p.fields

    def set_id():pass
       
    def set_title():pass
        
    def set_price():pass

    def set_delivery():pass

    def set_images():pass

    def set_combinations():pass

    def set_qty():pass

    def set_byer_protection():pass

    def set_description():pass

    def set_specification():pass

    def set_customer_reviews():pass

   
    #set_id(),
    #set_title(),
    #set_price(),
    #set_delivery(),
    #set_images(),
    #set_combinations(),
    #set_qty(),
    #set_byer_protection(),
    #set_description(),
    #set_specification(),
    #set_customer_reviews()
        
    return p
    pass



