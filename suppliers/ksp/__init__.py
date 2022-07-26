# -*- coding: utf-8 -*-
#!/usr/bin/env python
##@package Katia.suppliers.ksp
##
#Documentation for this module
#           Функции, присущие поставщику  KSP, которыми я дополняю класс supplier


import execute_json as json
from strings_formatter import StringFormatter as SF
from suppliers.product import Product 
import suppliers.ksp.banners_grabber
from script_logger import logger

def product_attributes(self, p, delimeter, elements):
    i=0
    skip = False
    c = p.combinations 
    ''' просто сокращенная запись '''
    for e in json.build_list_from_html_elements(self, delimeter, elements):
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
    
    ''' Вытаскиваю со страницы товара все поля по локаторам
            ------------
        p - товар
    '''
    
    def set_id():
        _id = _d.find(_['product_sku_locator'])
        '''
       Страница может не успеть подгрузиться AJAXом
       Я терпеливо пробую еще 5 раз.
        '''
        counter = 0 
        while _id is None:
            counter += 1
            _d.wait(10)
            _d._page_refresh()
            _id = _d.find(_['product_sku_locator'])
            logger.error(f'''{counter}. Не нашелся id 
            {_d.current_url}''')
            if counter > 5: break


        if _id is None: return False
        _field['id'] = _id
         
    def set_sku_suppl():
        _field['mkt suppl'] = _field['id']

    def set_sku_prod():
        if not _field['id']  is None :
            _field['mkt'] = str('ksp-') + _field['id']

    def set_title():
        title = _d.find(_['product_title_locator'])
        _field['title'] = SF.remove_non_latin_characters(title)

    def set_summary():
        _field['summary'] = _d.find(_['product_summary_locator'])

    def set_description():
        _field['description'] = _d.find(_['product_description_locator'])

    def set_cost_price():
        _price = _d.find(_['product_price_locator'])
        '''  Может прийти все, что угодно  
        Например, товара больше нет в наличии - цены не будет
        '''
        if _price is None:
            logger.error(f''' Не нашлась цена ''')
            return False

        _price = SF.clear_price(_price)
        _field['cost price'] =  _price
        logger.debug(f'''цена - {_field['cost price']}''')
        return True
    def set_before_tax_price():
        _field['price tax excluded']  = _field['cost price']
     
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

        _field['img url'] = p.get_certain_amount_of_images(s, imgs)
       
        
       

    def set_combinations():pass

    def set_qty():pass

    def set_specification():pass

    def set_customer_reviews():pass

    def set_supplier():
        _field['supplier'] = '2787'
        pass

    if not set_id(): return False
    set_sku_suppl()
    set_sku_prod()
    set_title()
    set_summary()
    if not set_cost_price(): return False
    set_before_tax_price()
    set_delivery()
    set_images()
    set_combinations()
    #set_qty()
    #set_byer_protection()
    set_description()
    #set_specification()
    #set_customer_reviews()
    set_supplier()
    return p
    pass



