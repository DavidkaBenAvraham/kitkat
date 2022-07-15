# -*- coding: utf-8 -*-
#!/usr/bin/env python
##@package Katia.suppliers.ksp
##
#Documentation for this module
#           Функции, присущие поставщику  KSP, которыми я дополняю класс supplier

 

from bs4 import BeautifulSoup
import execute_json as json
from strings_formatter import StringFormatter as SF
#formatter = StringFormatter()
from suppliers.product import Product 
import suppliers.ksp.banners_grabber
from loguru import logger

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

            attr = SF.remove_HTML_tags(e)
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

def grab_product_page(s , p) -> Product:
    p.grab_product_page(s)



    _ : dict = s.locators['product']
    _d = s.driver
    _d.scroll(3)
    _field = p.fields

    '''комбинации/опции товара '''
    _combinot = p.combinations
    
    
    ''' 
    Вытаскиваю со страницы товара все поля по локаторам
    ------------
    p - товар
    '''
    
    def set_id():
        _field['id'] = _d.find(_['product_sku_locator'])

    def set_mkt_suppl():
        _field['mkt_suppl'] = _field['id']

    def set_title():
        _field['title'] = _d.find(_['product_title_locator'])
        _field['title'] = SF.remove_non_latin_characters(_field['title'])
    
    def set_summary():
        _field['summary'] = _d.find(_['product_summary_locator'])

    def set_description():
        _field['description'] = _d.find(_['product_description_locator'])

    def set_price():
        _price = _d.find(_['product_price_locator'])
        try:
            '''  Может прийти все, что угодно  '''
            _price = SF.clear_price(_price)
        except Exception as ex: return False , print (f''' Exception   {ex} in set_price() ''')
        _field['mexir olut'] = _price
        return True

    def set_delivery():
        '''@TODO  перенести в комбинации '''
        product_delivery_list = _d.find(_['product_delivery_locator'])
        #for i in product_delivery_list:
        #    pass


    def set_images():
        #imgs_list  = _d.find(_['product_images_locator'])
        #imgs_str :str = ','.join(_d.find(_['product_images_locator']))
        imgs = _d.find(_['product_images_locator'])
        ''' может вернуться одна или несколько картинок или хуй.
        есть несколько ситуаций:
        - картинки нет на сайте
        - картинка не загрузилась (таймаут)
        - прочая хуйня
        '''
        if imgs is None: 
            _field['img url'] = ''
            return True
        elif isinstance(imgs , list):
            imgs = ','.join(imgs)
            _field['img url'] = imgs
        elif str(imgs)>0:_field['img url'] = imgs

        try:
            _field['img url'] = ','.join(imgs)
        except Exception as ex:
            logger.error(f'''ошибка в  _field['img url']  
            {ex}
            ''')
            _field['img url'] = ''


    def set_combinations():pass

    def set_qty():pass

    def set_byer_protection():pass

    

    def set_specification():pass

    def set_customer_reviews():pass

   
    set_id(),
    set_title(),
    set_summary()
    set_price(),
    set_delivery(),
    set_images(),
    set_combinations(),
    #set_qty(),
    #set_byer_protection(),
    set_description(),
    #set_specification(),
    #set_customer_reviews()
        
    return p
    pass



